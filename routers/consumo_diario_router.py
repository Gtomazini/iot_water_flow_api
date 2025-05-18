from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from models.consumo_diario_model import ConsumoDiarioCreate, ConsumoDiarioResponse
from models.consumo_diario_com_pontos_model import ConsumoDiarioComPontosResponse
from crud import consumo_diario as consumo_diario_crud

router = APIRouter()

@router.post("/consumo-diario/", response_model=ConsumoDiarioResponse)
def create_consumo_diario(consumo: ConsumoDiarioCreate, db: Session = Depends(get_db)):
    return consumo_diario_crud.create_consumo_diario(db=db, consumo=consumo)

@router.get("/consumo-diario/", response_model=List[ConsumoDiarioResponse])
def read_consumos_diarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consumos = consumo_diario_crud.get_consumos_diarios(db, skip=skip, limit=limit)
    return consumos

@router.get("/consumo-diario/{diario_id}", response_model=ConsumoDiarioResponse)
def read_consumo_diario(diario_id: int, db: Session = Depends(get_db)):
    db_consumo = consumo_diario_crud.get_consumo_diario(db, diario_id=diario_id)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="Registro de consumo diário não encontrado")
    return db_consumo

@router.get("/consumo-diario/{diario_id}/detalhado", response_model=ConsumoDiarioComPontosResponse)
def read_consumo_diario_detalhado(diario_id: int, db: Session = Depends(get_db)):
    db_consumo = consumo_diario_crud.get_consumo_diario_with_pontos(db, diario_id=diario_id)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="Registro de consumo diário não encontrado")
    return db_consumo

@router.get("/devices/{device_id}/consumo-diario/", response_model=List[ConsumoDiarioResponse])
def read_device_consumos_diarios(device_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consumos = consumo_diario_crud.get_device_consumos_diarios(db, device_id=device_id, skip=skip, limit=limit)
    return consumos

@router.put("/consumo-diario/{diario_id}", response_model=ConsumoDiarioResponse)
def update_consumo_diario(diario_id: int, consumo: ConsumoDiarioCreate, db: Session = Depends(get_db)):
    db_consumo = consumo_diario_crud.update_consumo_diario(db, diario_id=diario_id, consumo=consumo)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="Registro de consumo diário não encontrado")
    return db_consumo

@router.delete("/consumo-diario/{diario_id}", response_model=ConsumoDiarioResponse)
def delete_consumo_diario(diario_id: int, db: Session = Depends(get_db)):
    db_consumo = consumo_diario_crud.delete_consumo_diario(db, diario_id=diario_id)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="Registro de consumo diário não encontrado")
    return db_consumo

@router.post("/consumo-diario/{diario_id}/pontos/{ponto_id}", response_model=dict)
def add_ponto_to_consumo_diario(diario_id: int, ponto_id: int, db: Session = Depends(get_db)):
    result = consumo_diario_crud.add_ponto_to_consumo_diario(db, diario_id=diario_id, ponto_id=ponto_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Consumo diário ou ponto de consumo não encontrado")
    return {"message": "Ponto adicionado ao consumo diário com sucesso"}

@router.delete("/consumo-diario/{diario_id}/pontos/{ponto_id}", response_model=dict)
def remove_ponto_from_consumo_diario(diario_id: int, ponto_id: int, db: Session = Depends(get_db)):
    result = consumo_diario_crud.remove_ponto_from_consumo_diario(db, diario_id=diario_id, ponto_id=ponto_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Relação não encontrada")
    return {"message": "Ponto removido do consumo diário com sucesso"}