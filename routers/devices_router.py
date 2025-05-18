from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from models.device_model import DeviceCreate, DeviceResponse
from crud import device as device_crud

router = APIRouter()

@router.post("/devices/", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return device_crud.create_device(db=db, device=device)

@router.get("/devices/", response_model=List[DeviceResponse])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = device_crud.get_devices(db, skip=skip, limit=limit)
    return devices

@router.get("/devices/{device_id}", response_model=DeviceResponse)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = device_crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return db_device

@router.get("/users/{user_id}/devices/", response_model=List[DeviceResponse])
def read_user_devices(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = device_crud.get_user_devices(db, user_id=user_id, skip=skip, limit=limit)
    return devices

@router.put("/devices/{device_id}", response_model=DeviceResponse)
def update_device(device_id: int, device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = device_crud.update_device(db, device_id=device_id, device=device)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return db_device

@router.delete("/devices/{device_id}", response_model=DeviceResponse)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = device_crud.delete_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return db_device