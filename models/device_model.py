from pydantic import BaseModel, Field
from datetime import date
'''
Gabriel 11/04

DeviceCreate(BaseModel) cria um objeto para trabalhar com body herdando da basemodel do pydantic https://fastapi.tiangolo.com/tutorial/body/

'''


class DeviceCreate(BaseModel):
    id_user_vinc: int
    datetime_reg: date
    name_device: str = Field(..., max_length=255)

class DeviceResponse(BaseModel):
    id_device: int
    id_user_vinc: int
    datetime_reg: date
    name_device: str = Field(..., max_length=255)

    class Config:
        from_attributes = True