from pydantic import BaseModel


class CodigoUsuarioModel(BaseModel):
    id_codigo_usuario: int
    id_user: int
    codigo_user: str

    class Config:
        from_attributes = True


class CodigoUsuarioResponse(BaseModel):
    id_user: int

    class Config:
        from_attributes = True

class CodigoUsuarioCreate(BaseModel):
    id_user: int