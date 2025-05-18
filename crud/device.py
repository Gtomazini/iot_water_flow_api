from sqlalchemy.orm import Session
from schemas.device_schema import DeviceSchema
from models.device_model import DeviceCreate  # Alterado para DeviceCreate

def get_device(db: Session, device_id: int):
    return db.query(DeviceSchema).filter(DeviceSchema.id_device == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeviceSchema).offset(skip).limit(limit).all()

def get_user_devices(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(DeviceSchema).filter(
        DeviceSchema.id_user_vinc == user_id
    ).offset(skip).limit(limit).all()

def create_device(db: Session, device: DeviceCreate):  # Alterado para DeviceCreate
    db_device = DeviceSchema(
        id_user_vinc=device.id_user_vinc,
        datetime_reg=device.datetime_reg,
        name_device=device.name_device
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device(db: Session, device_id: int, device: DeviceCreate):
    db_device = get_device(db, device_id)
    if db_device:
        db_device.id_user_vinc = device.id_user_vinc
        db_device.datetime_reg = device.datetime_reg
        db_device.name_device = device.name_device
        db.commit()
        db.refresh(db_device)
    return db_device

def delete_device(db: Session, device_id: int):
    db_device = get_device(db, device_id)
    if db_device:
        db.delete(db_device)
        db.commit()
    return db_device