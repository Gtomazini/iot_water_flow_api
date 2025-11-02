from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from crud.codigo_usuario import create_codigo_usuario, deletar_codigo_usuario
from models.user_account_model import UserCreate, UserResponse
from crud import user_account as user_crud
from schemas.codigo_usuario_schema import CodigoUsuarioSchema

router = APIRouter()

@router.post("/users/", response_model=UserResponse, status_code=201)  # Deve retornar UserResponse com ID
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    novo_usuario = user_crud.create_user_account(db=db, user=user)
    codigo = create_codigo_usuario(db=db, id_user=novo_usuario.id_user)
    return {
        "id_user": novo_usuario.id_user,
        "username": novo_usuario.username,
        "locale": novo_usuario.locale,
        "codigo_user": codigo.codigo_user
    }


@router.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users_account(db, skip=skip, limit=limit)

    # Buscar os códigos para cada usuário
    users_with_codigo = []
    for user in users:
        codigo = db.query(CodigoUsuarioSchema).filter(
            CodigoUsuarioSchema.id_user == user.id_user
        ).first()

        users_with_codigo.append({
            "id_user": user.id_user,
            "username": user.username,
            "locale": user.locale,
            "codigo_user": codigo.codigo_user if codigo else None
        })

    return users_with_codigo

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_account_with_codigo(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)  # Deve retornar UserResponse com ID
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.update_user_account(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.delete("/users/{user_id}", response_model=UserResponse)  # Deve retornar UserResponse com ID
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    deletar_codigo_usuario(db=db, id_user=user_id)

    return db_user