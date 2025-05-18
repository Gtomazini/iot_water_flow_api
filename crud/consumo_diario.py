from sqlalchemy.orm import Session
from schemas.consumo_diario_schema import ConsumoDiarioSchema
from schemas.consumo_diario_pontos_schema import ConsumoDiarioPontosSchema
from schemas.consumo_pontos_schema import ConsumoPontosSchema
from models.consumo_diario_model import ConsumoDiarioCreate
from models.consumo_diario_com_pontos_model import ConsumoDiarioComPontosResponse


def get_consumo_diario(db: Session, diario_id: int):
    return db.query(ConsumoDiarioSchema).filter(
        ConsumoDiarioSchema.id_consumo_diario == diario_id
    ).first()


def get_consumos_diarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ConsumoDiarioSchema).offset(skip).limit(limit).all()


def get_device_consumos_diarios(db: Session, device_id: int, skip: int = 0, limit: int = 100):
    return db.query(ConsumoDiarioSchema).filter(
        ConsumoDiarioSchema.id_device_vinc == device_id
    ).offset(skip).limit(limit).all()


def create_consumo_diario(db: Session, consumo: ConsumoDiarioCreate):
    db_consumo = ConsumoDiarioSchema(
        id_device_vinc=consumo.id_device_vinc,
        volume_diario=consumo.volume_diario,
        datetime=consumo.datetime
    )
    db.add(db_consumo)
    db.commit()
    db.refresh(db_consumo)
    return db_consumo


def update_consumo_diario(db: Session, diario_id: int,
                          consumo: ConsumoDiarioCreate):  # Alterado para ConsumoDiarioCreate
    db_consumo = get_consumo_diario(db, diario_id)
    if db_consumo:
        db_consumo.id_device_vinc = consumo.id_device_vinc
        db_consumo.volume_diario = consumo.volume_diario
        db_consumo.datetime = consumo.datetime
        db.commit()
        db.refresh(db_consumo)
    return db_consumo


def delete_consumo_diario(db: Session, diario_id: int):
    db_consumo = get_consumo_diario(db, diario_id)
    if db_consumo:
        db.delete(db_consumo)
        db.commit()
    return db_consumo



def get_consumo_diario_with_pontos(db: Session, diario_id: int):
    db_consumo = get_consumo_diario(db, diario_id)

    if not db_consumo:
        return None


    pontos_consumo = db.query(ConsumoPontosSchema).join(
        ConsumoDiarioPontosSchema,
        ConsumoPontosSchema.id_consumo_ponto == ConsumoDiarioPontosSchema.id_consumo_ponto
    ).filter(
        ConsumoDiarioPontosSchema.id_consumo_diario == diario_id
    ).all()

    result = ConsumoDiarioComPontosResponse(
        id_consumo_diario=db_consumo.id_consumo_diario,
        id_device_vinc=db_consumo.id_device_vinc,
        volume_diario=db_consumo.volume_diario,
        datetime=db_consumo.datetime,
        pontos_consumo=pontos_consumo
    )

    return result



def add_ponto_to_consumo_diario(db: Session, diario_id: int, ponto_id: int):

    diario = get_consumo_diario(db, diario_id)
    ponto = db.query(ConsumoPontosSchema).filter(ConsumoPontosSchema.id_consumo_ponto == ponto_id).first()

    if not diario or not ponto:
        return None


    existing = db.query(ConsumoDiarioPontosSchema).filter(
        ConsumoDiarioPontosSchema.id_consumo_diario == diario_id,
        ConsumoDiarioPontosSchema.id_consumo_ponto == ponto_id
    ).first()

    if existing:
        return existing


    db_relacao = ConsumoDiarioPontosSchema(
        id_consumo_diario=diario_id,
        id_consumo_ponto=ponto_id
    )
    db.add(db_relacao)
    db.commit()
    return db_relacao


def remove_ponto_from_consumo_diario(db: Session, diario_id: int, ponto_id: int):
    db_relacao = db.query(ConsumoDiarioPontosSchema).filter(
        ConsumoDiarioPontosSchema.id_consumo_diario == diario_id,
        ConsumoDiarioPontosSchema.id_consumo_ponto == ponto_id
    ).first()
    if db_relacao:
        db.delete(db_relacao)
        db.commit()
    return db_relacao