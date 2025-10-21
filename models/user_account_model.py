from pydantic import BaseModel, Field
'''
Gabriel 11/04

UserCreate(BaseModel) cria um objeto para trabalhar com body herdando da basemodel do pydantic https://fastapi.tiangolo.com/tutorial/body/

'''


class UserCreate(BaseModel):
    username: str = Field(..., max_length=255)
    locale: str = Field(..., max_length=255)

class UserResponse(BaseModel):
    id_user: int
    username: str = Field(..., max_length=255)
    locale: str = Field(..., max_length=255)
    codigo_user: str

    class Config:
        from_attributes = True

