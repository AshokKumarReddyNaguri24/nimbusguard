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
