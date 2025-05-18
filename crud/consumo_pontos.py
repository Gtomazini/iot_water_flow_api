from sqlalchemy.orm import Session
from schemas.consumo_pontos_schema import ConsumoPontosSchema
from models.consumo_pontos_model import ConsumoPontosCreate

def get_consumo_ponto(db: Session, ponto_id: int):
    return db.query(ConsumoPontosSchema).filter(
        ConsumoPontosSchema.id_consumo_ponto == ponto_id
    ).first()

def get_consumos_pontos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ConsumoPontosSchema).offset(skip).limit(limit).all()

def get_device_consumos_pontos(db: Session, device_id: int, skip: int = 0, limit: int = 100):
    return db.query(ConsumoPontosSchema).filter(
        ConsumoPontosSchema.id_device_vinc == device_id
    ).offset(skip).limit(limit).all()

def create_consumo_ponto(db: Session, consumo: ConsumoPontosCreate):
    db_consumo = ConsumoPontosSchema(
        id_device_vinc=consumo.id_device_vinc,
        consumo_pontos=consumo.consumo_pontos,
        datetime=consumo.datetime
    )
    db.add(db_consumo)
    db.commit()
    db.refresh(db_consumo)
    return db_consumo

def update_consumo_ponto(db: Session, ponto_id: int, consumo: ConsumoPontosCreate):
    db_consumo = get_consumo_ponto(db, ponto_id)
    if db_consumo:
        db_consumo.id_device_vinc = consumo.id_device_vinc
        db_consumo.consumo_pontos = consumo.consumo_pontos
        db_consumo.datetime = consumo.datetime
        db.commit()
        db.refresh(db_consumo)
    return db_consumo

def delete_consumo_ponto(db: Session, ponto_id: int):
    db_consumo = get_consumo_ponto(db, ponto_id)
    if db_consumo:
        db.delete(db_consumo)
        db.commit()
    return db_consumo