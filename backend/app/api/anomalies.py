from fastapi import APIRouter
from app.config.logging import get_logger
from app.models import anomaly as schemas

router = APIRouter()
logger = get_logger(__name__)


@router.post("/ingest")
def ingest_anomaly(event: schemas.AnomalyEvent):
    logger.warning(
        "Anomaly ingest: device_id=%s metric=%s value=%s score=%s threshold=%s source=%s time=%s",
        event.device_id,
        event.metric_name,
        event.value,
        event.score,
        event.threshold,
        event.source,
        event.time,
    )
    if event.details:
        logger.info("Anomaly details: device_id=%s details=%s", event.device_id, event.details)
    return {"status": "logged"}
