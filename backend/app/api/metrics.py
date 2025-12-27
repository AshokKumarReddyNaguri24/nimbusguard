from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import database
from app.models import metric as schemas # using schemas alias for convenience or rename to models
from datetime import datetime, timezone

router = APIRouter()

@router.post("/post")
def create_metric(metric: schemas.MetricCreate, db: Session = Depends(database.get_db_metrics)):
    # Validate device exists in Inventory DB? 
    # Optional performance trade-off. For now, we trust the collector or separate validation.
    
    # Insert into TimescaleDB
    # Using raw SQL for efficiency and simple hypertable interaction
    try:
        current_time = datetime.utcnow()
        query = text("""
            INSERT INTO metrics (time, device_id, metric_name, value)
            VALUES (:time, :device_id, :metric_name, :value)
        """)
        db.execute(query, {
            "time": current_time, 
            "device_id": metric.device_id, 
            "metric_name": metric.metric_name, 
            "value": metric.metric_value
        })
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
