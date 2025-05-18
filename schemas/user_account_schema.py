from sqlalchemy import Column, Integer, String
from schemas.base import Base

class UserAccountSchema(Base):
    __tablename__ = 'user_account'
    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    locale = Column(String(255), nullable=False)
