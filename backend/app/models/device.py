from sqlalchemy import Column, Integer, String
from app.config.database import Base
from pydantic import BaseModel
from typing import Optional

# --- SQLAlchemy Models ---
class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String, index=True)
    device_type = Column(String)
    location = Column(String, nullable=True)

# --- Pydantic Schemas ---
class DeviceBase(BaseModel):
    name: str
    ip_address: str
    device_type: str
    location: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceResponse(DeviceBase):
    id: int

    class Config:
        from_attributes = True # updated for Pydantic v2 support (was orm_mode)

