from sqlalchemy.orm import Session

from schemas.codigo_usuario_schema import CodigoUsuarioSchema
from schemas.user_account_schema import UserAccountSchema
from models.user_account_model import UserCreate

def get_user_account(db: Session, user_id: int):
    return db.query(UserAccountSchema).filter(UserAccountSchema.id_user == user_id).first()

def get_users_account(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserAccountSchema).offset(skip).limit(limit).all()

def create_user_account(db: Session, user: UserCreate):
    db_user = UserAccountSchema(
        username=user.username,
        locale=user.locale
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_account_with_codigo(db: Session, user_id: int):
    user = db.query(UserAccountSchema).filter(UserAccountSchema.id_user == user_id).first()
    if not user:
        return None

    codigo = db.query(CodigoUsuarioSchema).filter(
        CodigoUsuarioSchema.id_user == user_id
    ).first()

    return {
        "id_user": user.id_user,
        "username": user.username,
        "locale": user.locale,
        "codigo_user": codigo.codigo_user if codigo else None
    }

def update_user_account(db: Session, user_id: int, user: UserCreate):
    db_user = get_user_account(db, user_id)
    if db_user:
        db_user.username = user.username
        db_user.locale = user.locale
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user_account(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user