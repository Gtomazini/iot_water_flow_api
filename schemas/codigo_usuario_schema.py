from sqlalchemy import Column, Integer, ForeignKey, String

from schemas.base import Base


class CodigoUsuarioSchema(Base):
    __tablename__ = 'codigo_usuario'

    id_codigo_usuario = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey('user_account.id_user'), nullable= False)
    codigo_user = Column(String(255), nullable=False)
