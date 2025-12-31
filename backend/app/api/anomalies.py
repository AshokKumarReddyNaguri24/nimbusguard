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
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services import anomaly_service

router = APIRouter()

class AnomalyCheckRequest(BaseModel):
    device_id: int
    metric_type: str

@router.post("/check")
async def check_anomaly(request: AnomalyCheckRequest):
    """
    Manually trigger an anomaly check for a specific device and metric.
    """
    result = anomaly_service.check_device_metric(request.device_id, request.metric_type)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
    return result

