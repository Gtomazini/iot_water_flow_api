from fastapi.testclient import TestClient

from app.main import app

'''
    Gabriel 11/04
    test_root_access() - teste de acesso ao serviço no endpoint base /
    
    doc do testclient: https://fastapi.tiangolo.com/reference/testclient/
'''

client = TestClient(app)

def test_root_access():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API com acesso limitado ao Projeto Integrador V UNIVESP"}