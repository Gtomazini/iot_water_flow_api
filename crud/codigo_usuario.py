from sqlalchemy.orm import Session

from schemas.codigo_usuario_schema import CodigoUsuarioSchema
from utils.gerador_codigo import gerar_codigo_aleatorio


def codigo_retorno_id_user(db: Session, codigo_usuario: str):
    return db.query(CodigoUsuarioSchema).filter(
        CodigoUsuarioSchema.codigo_user == codigo_usuario
    ).first()

def get_codigo_usuario(db: Session):
    return db.query(CodigoUsuarioSchema).all()

def create_codigo_usuario(db: Session, id_user: int):

    while True:
        codigo_user = gerar_codigo_aleatorio()

        existe = db.query(CodigoUsuarioSchema).filter(
            CodigoUsuarioSchema.codigo_user == codigo_user
        ).first()
        if not existe:
            break

    novo_codigo = CodigoUsuarioSchema(
        id_user = id_user,
        codigo_user=codigo_user
    )
    db.add(novo_codigo)
    db.commit()
    db.refresh(novo_codigo)
    return novo_codigo

def delete_codigo_usuario(db: Session, id_user:int):

    target = db.query(CodigoUsuarioSchema).filter(
        CodigoUsuarioSchema.id_user == id_user
    ).first()

    if not target:
        return None
    db.delete(target)
    db.commit()
    return True