from sqlalchemy import Column, Integer, TIMESTAMP, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from schemas.base import Base


class ConsumoPontosSchema(Base):
    __tablename__ = 'consumo_pontos'

    id_consumo_ponto = Column(Integer, primary_key=True, index=True)
    id_device_vinc = Column(Integer, ForeignKey('device.id_device'), nullable=False)
    consumo_pontos = Column(Numeric(10, 6), nullable=False)
    datetime = Column(DateTime, nullable=False, default=func.now())