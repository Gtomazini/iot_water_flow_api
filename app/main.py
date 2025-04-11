from fastapi import FastAPI
from models.sensor import SensorModel
'''
Ponto de entrada da API
Gabriel 11/04

app instancia uma aplicação FastAPI
def root() cria o primeiro endpoint

mais detalhes consultar em: https://fastapi.tiangolo.com/tutorial/first-steps/#step-2-create-a-fastapi-instance

sensor_stock() consulta de dispostivo registrado
parametros no endpoint: https://fastapi.tiangolo.com/tutorial/path-params/

sensor_stock_read() - por enquanto conforme os testes ele só retorna o objeto

'''

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API com acesso limitado ao Projeto Integrador V UNIVESP"}

@app.get("/sensor/{sensor_id}")
async def sensor_stock(sensor_id):
    return {"sensor_id": sensor_id}

@app.post("/sensor")
def sensor_stock_read(sensor: SensorModel):
    return {"sensor_id" : sensor.sensor_id}
