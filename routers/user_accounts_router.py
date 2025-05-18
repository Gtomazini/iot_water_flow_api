from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from models.user_account_model import UserCreate, UserResponse
from crud import user_account as user_crud

router = APIRouter()

@router.post("/users/", response_model=UserResponse)  # Deve retornar UserResponse com ID
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user_account(db=db, user=user)

@router.get("/users/", response_model=List[UserResponse])  # Deve retornar UserResponse com ID
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users_account(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_account(db, user_id=user_id)
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
    return db_user