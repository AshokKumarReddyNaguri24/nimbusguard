from pydantic import BaseModel
from typing import Any

class MetricCreate(BaseModel):
    device_id: int
    metric_name: str
    value: float
    time: Any = None # Optional, will default to current time in DB if not provided
