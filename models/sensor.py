from pydantic import BaseModel

'''
Gabriel 11/04

SensorModel(BaseModel) cria um objeto para trabalhar com body herdando da basemodel do pydantic https://fastapi.tiangolo.com/tutorial/body/

'''
class SensorModel(BaseModel):
    sensor_id: str