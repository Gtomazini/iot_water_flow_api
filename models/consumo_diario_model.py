from datetime import date
from pydantic import BaseModel, condecimal, Field
from typing import Optional

'''
ConsumoDiarioBase - Modelo base com campos comuns
ConsumoDiarioCreate - Modelo para receber dados na criação (sem ID)
ConsumoDiarioResponse - Modelo completo para respostas (com ID)
'''

class ConsumoDiarioBase(BaseModel):
    """Campos comuns a todas as operações"""
    id_device_vinc: int
    volume_diario: condecimal(ge=0, decimal_places=6, max_digits=10)
    datetime: date

class ConsumoDiarioCreate(ConsumoDiarioBase):
    """Modelo para criar resumos diários (sem ID)"""
    pass

class ConsumoDiarioResponse(ConsumoDiarioBase):
    """Modelo completo incluindo o ID (para respostas)"""
    id_consumo_diario: int

    class Config:
        from_attributes = True  # Para Pydantic v2