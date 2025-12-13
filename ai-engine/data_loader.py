import psycopg2
import pandas as pd
import os
from datetime import datetime, timedelta


def get_db_connection(): #Creating connection to TimescaleDB using environment variables
    
    return psycopg2.connect(
        host=os.getenv('TIMESCALE_DB_HOST', 'timescaledb'),
        port=os.getenv('TIMESCALE_DB_PORT', '5432'),
        database=os.getenv('TIMESCALE_DB_NAME', 'postgres'),
        user=os.getenv('TIMESCALE_DB_USER', 'admin'),
        password=os.getenv('TIMESCALE_DB_PASS', 'admin')
    )

def load_metrics(device_id=None, metric_type=None, hours=24):
  
    try:
        conn = get_db_connection()
        
        query = """ 
            SELECT timestamp, device_id, metric_type, value  
            FROM metrics
            WHERE timestamp >= NOW() - INTERVAL '%s hours'
        """
        params = [hours]
        
        if device_id:
            query += " AND device_id = %s"
            params.append(device_id)
        
        if metric_type:
            query += " AND metric_type = %s"
            params.append(metric_type)
        
        query += " ORDER BY timestamp DESC"
        
        df = pd.read_sql_query(query, conn, params=params)   # Load data
        conn.close()
        
        print(f"✓ Loaded {len(df)} metrics from TimescaleDB")
        return df
        
    except Exception as e:
        print(f"✗ Failed to load metrics: {e}")
        return pd.DataFrame()


def test_connection(): #Test if we can connect to TimescaleDB
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM metrics;")
        count = cursor.fetchone()[0]
        print(f"✓ Connected! Found {count} metrics in database")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()
    
    df = load_metrics(hours=24) #load test data
    if not df.empty:
        print("\nSample data:")
        print(df.head())
