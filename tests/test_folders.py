from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.main import app
from app.config import API_KEY_NAME, API_KEY_VALUE


client = TestClient(app)


def test_get_folders_denied():
    response = client.get('/folders/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_post_folders_denied():
    response = client.post('/folders/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_patch_folders_denied():
    response = client.patch('/folders/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_delete_folders_denied():
    response = client.delete('/folders/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_get_file_denied():
    response = client.get('/folders/file/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_post_file_denied():
    response = client.post('/folders/file/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_patch_file_denied():
    response = client.patch('/folders/file/')
    assert response.status_code == HTTP_401_UNAUTHORIZED


def test_delete_file_denied():
    response = client.delete('/folders/file/')
    assert response.status_code == HTTP_401_UNAUTHORIZED
