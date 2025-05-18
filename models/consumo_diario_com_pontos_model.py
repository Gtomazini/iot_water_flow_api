from typing import List

from models.consumo_diario_model import ConsumoDiarioResponse
from models.consumo_pontos_model import ConsumoPontosResponse

'''
ConsumoDiarioComPontosResponse - Modelo que estende ConsumoDiarioResponse
incluindo uma lista de pontos de consumo relacionados
'''

class ConsumoDiarioComPontosResponse(ConsumoDiarioResponse):
    """Modelo para respostas que incluem consumo diário e seus pontos relacionados"""
    pontos_consumo: List[ConsumoPontosResponse] = []

    class Config:
        from_attributes = True  # Para Pydantic v2