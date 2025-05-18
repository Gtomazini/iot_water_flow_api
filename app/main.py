from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar engine para conexão com o banco
from app.database import engine

# Importar Base dos schemas para criar tabelas
from schemas.user_account_schema import Base as UserBase
from schemas.device_schema import Base as DeviceBase
from schemas.consumo_pontos_schema import Base as ConsumoPontosBase
from schemas.consumo_diario_schema import Base as ConsumoDiarioBase
from schemas.consumo_diario_pontos_schema import Base as ConsumoDiarioPontosBase

# Importar os roteadores
from routers.user_accounts_router import router as user_router
from routers.devices_router import router as device_router
from routers.consumo_pontos_router import router as consumo_pontos_router
from routers.consumo_diario_router import router as consumo_diario_router

'''
Ponto de entrada da API
Gabriel 11/04 (atualizado em [data atual])

app instancia uma aplicação FastAPI
Configurações adicionais incluem CORS e metadata da API
Inclui todos os roteadores para as diferentes entidades

mais detalhes consultar em: https://fastapi.tiangolo.com/tutorial/first-steps/
'''

# Criar as tabelas no banco de dados
# Comentar estas linhas em produção ou se as tabelas já existirem
UserBase.metadata.create_all(bind=engine)
DeviceBase.metadata.create_all(bind=engine)
ConsumoPontosBase.metadata.create_all(bind=engine)
ConsumoDiarioBase.metadata.create_all(bind=engine)
ConsumoDiarioPontosBase.metadata.create_all(bind=engine)

app = FastAPI(
    title="WaterGame API",
    description="API com acesso limitado ao Projeto Integrador V UNIVESP - Sistema de monitoramento de consumo de água",
    version="1.0.0"
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Requisição recebida: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Resposta enviada: {response.status_code}")
    return response

# Incluir roteadores
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(device_router, prefix="/api/v1", tags=["devices"])
app.include_router(consumo_pontos_router, prefix="/api/v1", tags=["consumo_pontos"])
app.include_router(consumo_diario_router, prefix="/api/v1", tags=["consumo_diario"])

# Endpoint raiz
@app.get("/")
async def root():
    return {
        "message": "API com acesso limitado ao Projeto Integrador V UNIVESP",
        "documentation": "/docs",
        "redoc": "/redoc"
    }