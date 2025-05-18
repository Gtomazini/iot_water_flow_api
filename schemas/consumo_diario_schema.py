from sqlalchemy import Column, Integer, TIMESTAMP, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from schemas.base import Base


class ConsumoDiarioSchema(Base):
    __tablename__ = 'consumo_diario'

    id_consumo_diario = Column(Integer, primary_key=True, index=True)
    id_device_vinc = Column(Integer, ForeignKey('device.id_device'), nullable=False)
    volume_diario = Column(Numeric(10, 6), nullable=False)
    datetime = Column(DateTime)