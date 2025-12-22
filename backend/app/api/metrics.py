from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import database
from app.config.logging import get_logger
from app.config.settings import settings
from app.models import metric as schemas # using schemas alias for convenience or rename to models
from datetime import datetime

logger = get_logger(__name__)

ANOMALY_THRESHOLDS = {
    "cpu_usage": settings.ANOMALY_THRESHOLD_CPU,
    "memory_usage": settings.ANOMALY_THRESHOLD_MEMORY,
}

router = APIRouter()

@router.post("/post")
def create_metric(metric: schemas.MetricCreate, db: Session = Depends(database.get_db_metrics)):
    # Validate device exists in Inventory DB? 
    # Optional performance trade-off. For now, we trust the collector or separate validation.
    
    # Insert into TimescaleDB
    # Using raw SQL for efficiency and simple hypertable interaction
    try:
        event_time = metric.time or datetime.utcnow()
        query = text("""
            INSERT INTO metrics (time, device_id, metric_name, value)
            VALUES (:time, :device_id, :metric_name, :value)
        """)
        db.execute(query, {
            "time": event_time,
            "device_id": metric.device_id,
            "metric_name": metric.metric_name,
            "value": metric.value,
        })
        db.commit()

        threshold = ANOMALY_THRESHOLDS.get(metric.metric_name)
        if threshold is not None and metric.value >= threshold:
            logger.warning(
                "Anomaly detected: device_id=%s metric=%s value=%s threshold=%s",
                metric.device_id,
                metric.metric_name,
                metric.value,
                threshold,
            )
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        logger.error("Metric insert failed", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
