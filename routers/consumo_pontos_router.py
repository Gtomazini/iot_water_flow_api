from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from models.consumo_pontos_model import ConsumoPontosCreate, ConsumoPontosResponse
from crud import consumo_pontos as consumo_pontos_crud

router = APIRouter()

@router.post("/consumo-pontos/", response_model=ConsumoPontosResponse)
def create_consumo_ponto(consumo: ConsumoPontosCreate, db: Session = Depends(get_db)):
    return consumo_pontos_crud.create_consumo_ponto(db=db, consumo=consumo)

@router.get("/consumo-pontos/", response_model=List[ConsumoPontosResponse])
def read_consumos_pontos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consumos = consumo_pontos_crud.get_consumos_pontos(db, skip=skip, limit=limit)
    return consumos

@router.get("/consumo-pontos/{ponto_id}", response_model=ConsumoPontosResponse)
def read_consumo_ponto(ponto_id: int, db: Session = Depends(get_db)):
    db_consumo = consumo_pontos_crud.get_consumo_ponto(db, ponto_id=ponto_id)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="Registro de consumo não encontrado")
    return db_consumo

@router.get("/devices/{device_id}/consumo-pontos/", response_model=List[ConsumoPontosResponse])
def read_device_consumos_pontos(device_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consumos = consumo_pontos_crud.get_device_consumos_pontos(db, device_id=device_id, skip=skip, limit=limit)
    return consumos

@router.put("/consumo-pontos/{ponto_id}", response_model=ConsumoPontosResponse)
def update_consumo_ponto(ponto_id: int, consumo: ConsumoPontosCreate, db: Session = Depends(get_db)):
    db_consumo = consumo_pontos_crud.update_consumo_ponto(db, ponto_id=ponto_id, consumo=consumo)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="Registro de consumo não encontrado")
    return db_consumo

@router.delete("/consumo-pontos/{ponto_id}", response_model=ConsumoPontosResponse)
def delete_consumo_ponto(ponto_id: int, db: Session = Depends(get_db)):
    db_consumo = consumo_pontos_crud.delete_consumo_ponto(db, ponto_id=ponto_id)
    if db_consumo is None:
        raise HTTPException(status_code=404, detail="Registro de consumo não encontrado")
    return db_consumo