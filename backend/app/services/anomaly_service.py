import pandas as pd
import numpy as np
import os
import psycopg2
from app.config.database import SessionLocal
from app.models.alert import Alert
from app.models.device import Device
from sqlalchemy.orm import Session
from datetime import datetime

from app.config.settings import settings

# --- 1. DATA LOADER (Duplicated from ai-engine/data_loader.py to avoid import issues) ---
def get_db_connection():
    return psycopg2.connect(
        host=settings.TSDB_HOST,
        port=settings.TSDB_PORT,
        database=settings.TSDB_NAME,
        user=settings.TSDB_USER,
        password=settings.TSDB_PASS
    )

def load_metrics(device_id=None, metric_type=None, hours=24):
    try:
        conn = get_db_connection()
        query = """ 
            SELECT time, device_id, metric_name, value  
            FROM metrics
            WHERE time >= NOW() - INTERVAL '%s hours'
        """
        params = [hours]
        
        if device_id:
            query += " AND device_id = %s"
            params.append(device_id)
        
        if metric_type:
            query += " AND metric_name = %s"
            params.append(metric_type)
        
        query += " ORDER BY time DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        print(f"Error loading metrics: {e}")
        return pd.DataFrame()

# --- 2. AI LOGIC (Duplicated from ai-engine/baseline_model.py) ---
def calculate_baseline(data):
    if len(data) == 0:
        return {'mean': 0, 'std': 1, 'median': 0}
    return {
        'mean': np.mean(data),
        'std': np.std(data),
        'median': np.median(data)
    }

def detect_anomalies(data, baseline, threshold=2):
    anomalies = []
    mean = baseline['mean']
    std = baseline['std']
    
    if std == 0: return []

    for i, value in enumerate(data):
        z_score = abs((value - mean) / std)
        if z_score > threshold:
            anomalies.append({
                'index': i,
                'value': value,
                'z_score': z_score
            })            
    return anomalies

# --- 3. SERVICE LOGIC ---
def create_alert(db: Session, device_id: int, metric_type: str, value: float, description: str):
    # Check if duplicate unresolved alert exists recently to avoid spam could be added here
    alert = Alert(
        device_id=device_id,
        metric_type=metric_type,
        value=value,
        description=description,
        resolved=False
    )
    db.add(alert)
    db.commit()
    return alert

def check_device_metric(device_id: int, metric_type: str, db: Session = None):
    """
    Checks for anomalies for a specific device and metric.
    Returns list of detected anomalies.
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    
    try:
        # 1. Load Data
        df = load_metrics(device_id=device_id, metric_type=metric_type, hours=24)
        if df.empty or len(df) < 10: # Need enough data
            return {"status": "insufficient_data"}

        data = df['value'].values
        
        # 2. Calculate Baseline
        baseline = calculate_baseline(data)
        
        # 3. Detect Anomalies (check last few points, or just the latest)
        # For simplicity in this loop, we might just check the LATEST point to create an alert
        # But detect_anomalies returns all.
        anomalies = detect_anomalies(data, baseline)
        
        latest_anomaly = None
        
        # Filter for recent anomalies (e.g., in the last 5 minutes) or just check if the NEWEST point is anomalous
        # df is ordered DESC, so index 0 is latest.
        if anomalies:
            # Check if index 0 is in anomalies list
            # anomalies is a list of dicts with 'index'
            latest_idx = 0 
            is_latest_anomalous = any(a['index'] == latest_idx for a in anomalies)
            
            if is_latest_anomalous:
                latest_val = data[0]
                desc = f"Anomaly detected for {metric_type}. Value: {latest_val:.2f} (Mean: {baseline['mean']:.2f}, Z-Score > 2)"
                create_alert(db, device_id, metric_type, latest_val, desc)
                latest_anomaly = {"value": latest_val, "description": desc}
                print(f"ALERT CREATED: {desc}")
        
        return {
            "status": "checked", 
            "baseline": {k: float(v) for k, v in baseline.items()}, # convert numpy types
            "anomaly": latest_anomaly
        }

    except Exception as e:
        print(f"Error in check_device_metric: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        if close_db:
            db.close()

def run_anomaly_checks():
    """
    Scheduled job: Iterates all devices and metrics.
    """
    print("Running scheduled anomaly checks...")
    db = SessionLocal()
    try:
        devices = db.query(Device).all()
        metric_types = ["cpu", "memory", "latency"] # Define what to check
        
        for device in devices:
            for m_type in metric_types:
                check_device_metric(device.id, m_type, db)
                
    except Exception as e:
        print(f"Scheduler Check Failed: {e}")
    finally:
        db.close()
