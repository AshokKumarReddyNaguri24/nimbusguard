from pydantic import BaseModel
from typing import Any, Dict, Optional


class AnomalyEvent(BaseModel):
    device_id: int
    metric_name: str
    value: float
    score: Optional[float] = None
    threshold: Optional[float] = None
    source: Optional[str] = None
    time: Optional[Any] = None
    details: Optional[Dict[str, Any]] = None
