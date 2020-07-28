from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.main import app
from app.config import API_KEY_NAME, API_KEY_VALUE


client = TestClient(app)


def test_access_set_cookie_denied():
    response = client.get('/access/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_access_delete_cookie_denied():
    response = client.delete('/access/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_access_set_cookie_api_key_query():
    response = client.get(f'/access/?{API_KEY_NAME}={API_KEY_VALUE}')
    assert response.status_code == HTTP_200_OK
    assert response.cookies.get(API_KEY_NAME) == API_KEY_VALUE


def test_access_set_cookie_api_key_header():
    response = client.get('/access/', headers={API_KEY_NAME: API_KEY_VALUE})
    assert response.status_code == HTTP_200_OK
    assert response.cookies.get(API_KEY_NAME) == API_KEY_VALUE


def test_access_set_cookie_api_key_cookie():
    response = client.get('/access/', cookies={API_KEY_NAME: API_KEY_VALUE})
    assert response.status_code == HTTP_200_OK
    assert response.cookies.get(API_KEY_NAME) == API_KEY_VALUE


def test_access_delete_cookie_api_key_query():
    response = client.delete(f'/access/?{API_KEY_NAME}={API_KEY_VALUE}')
    assert response.status_code == HTTP_200_OK


def test_access_delete_cookie_api_key_header():
    response = client.delete('/access/', headers={API_KEY_NAME: API_KEY_VALUE})
    assert response.status_code == HTTP_200_OK


def test_access_delete_cookie_api_key_cookie():
    response = client.delete('/access/', cookies={API_KEY_NAME: API_KEY_VALUE})
    assert response.status_code == HTTP_200_OK
