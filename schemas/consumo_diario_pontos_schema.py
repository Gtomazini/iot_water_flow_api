from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from schemas.base import Base


class ConsumoDiarioPontosSchema(Base):
    __tablename__ = 'consumo_diario_pontos'

    id_consumo_diario = Column(Integer, ForeignKey('consumo_diario.id_consumo_diario'))
    id_consumo_ponto = Column(Integer, ForeignKey('consumo_pontos.id_consumo_ponto'))

    # Define uma chave primária composta
    __table_args__ = (
        PrimaryKeyConstraint('id_consumo_diario', 'id_consumo_ponto'),
    )