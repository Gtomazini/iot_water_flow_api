from fastapi import FastAPI

'''
Ponto de entrada da API
Gabriel 11/04

app instancia uma aplicação FastAPI
def root() cria o primeiro endpoint

mais detalhes consultar em: https://fastapi.tiangolo.com/tutorial/first-steps/#step-2-create-a-fastapi-instance
'''

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API com acesso limitado ao Projeto Integrador V UNIVESP"}