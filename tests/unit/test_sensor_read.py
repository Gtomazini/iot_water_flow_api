from fastapi.testclient import TestClient

from app.main import app

'''
    Gabriel 11/04
    test_sensor_read() - teste para verificar o registro do sensor

    doc do testclient: https://fastapi.tiangolo.com/reference/testclient/
'''

client = TestClient(app)

# url
def test_sensor_read():
    target_sensor = "AG100"
    response = client.get(f"/sensor/{target_sensor}")
    assert response.status_code == 200
    assert response.json() == {"sensor_id": "AG100"}

def test_sensor_read_body():
    target_sensor = "AG100"
    response = client.post("/sensor", json={"sensor_id": f"{target_sensor}"})
    assert response.status_code == 200
    assert response.json() == {"sensor_id": "AG100"}


# ainda n tem como aplicar esse cara
'''
def test_sensor_not_read():
    target_sensor = "AX800"
    response = client.get(f"/sensor/{target_sensor}")
    assert response.status_code == 401
'''