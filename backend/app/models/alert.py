from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from app.config.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, nullable=True) # ForeignKey("devices.id") - keeping loose for now or strictly linking
    metric_type = Column(String, index=True)
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(Text)
    resolved = Column(Boolean, default=False)
