from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from schemas.base import Base


class DeviceSchema(Base):
    __tablename__ = 'device'

    id_device = Column(Integer, primary_key=True, index=True)
    id_user_vinc = Column(Integer, ForeignKey('user_account.id_user'), nullable=False)
    datetime_reg = Column(DateTime, default=datetime.utcnow)  # Corrigido para DateTime
    name_device = Column(String(255), nullable=False)