from pydantic import BaseModel, Field, condecimal
from datetime import date, datetime
from typing import Optional

'''
Gabriel 11/04
Atualizado para seguir o padrão de modelos separados para entrada e saída

ConsumoPontosBase - Modelo base com campos comuns
ConsumoPontosCreate - Modelo para receber dados na criação (sem ID)
ConsumoPontosResponse - Modelo completo para respostas (com ID)
'''

class ConsumoPontosBase(BaseModel):
    id_device_vinc: int
    consumo_pontos: condecimal(ge=0, decimal_places=6, max_digits=10)
    datetime: datetime

class ConsumoPontosCreate(ConsumoPontosBase):
    pass

class ConsumoPontosResponse(ConsumoPontosBase):
    id_consumo_ponto: int

    class Config:
        from_attributes = True  # Para Pydantic v2