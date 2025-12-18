from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.config import database
from app.models import device as models

router = APIRouter()

@router.get("/all", response_model=List[models.DeviceResponse]) # The user asked for /devices/all, so if this router is mounted at /devices, this should be /all
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db_inventory)):
    devices = db.query(models.Device).offset(skip).limit(limit).all()
    return devices

@router.post("/add", response_model=models.DeviceResponse)
def create_device(device: models.DeviceCreate, db: Session = Depends(database.get_db_inventory)):
    db_device = db.query(models.Device).filter(models.Device.name == device.name).first()
    if db_device:
        raise HTTPException(status_code=400, detail="Device already registered")
    
    new_device = models.Device(
        name=device.name,
        ip_address=device.ip_address,
        device_type=device.device_type,
        location=device.location
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device
