

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from crud.codigo_usuario import codigo_retorno_id_user, create_codigo_usuario
from models.codigo_usuario_model import CodigoUsuarioResponse, CodigoUsuarioModel, CodigoUsuarioCreate

router = APIRouter()

@router.post("/codigo-usuario/{codigo_user}", response_model=CodigoUsuarioResponse)
def return_user_code(codigo_user: str, db: Session = Depends(get_db)):
    result = codigo_retorno_id_user(db=db, codigo_usuario=codigo_user)

    if not result:
        raise HTTPException(status_code=404, detail="Código de usuário não encontrado")

    return result

@router.post("/codigo-usuario/create/{id_user", response_model=CodigoUsuarioModel, status_code=201)
def create_new_codigo_usuario(codigo_data: CodigoUsuarioCreate, db: Session = Depends(get_db)):
    return create_codigo_usuario(db=db, id_user=codigo_data.id_user)

@router.get("/codigo-usuario", response_model=list[CodigoUsuarioModel])
def get_all_codigo_usuario(db: Session = Depends(get_db)):
    return get_all_codigo_usuario(db=db)

@router.delete("/codigo-usuario/{id_user}")
def delete_codigo_usuario(id_user: int, db: Session = Depends(get_db)):
    result = delete_codigo_usuario(db=db, id_user=id_user)

    if not result:
        raise HTTPException(status_code=404, detail="Código de usuário não encontrado")

    return {"message": "Código de usuário removido com sucesso"}



