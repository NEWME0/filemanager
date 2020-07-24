from fastapi.testclient import TestClient
from starlette import status
from app.__main__ import app


client = TestClient(app)



def test_main():
    response = client.get('/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_apikey_less():
    response = client.get('/apikey')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_apikey_set_cookie():
    response = client.get(f'/apikey?access-token=')