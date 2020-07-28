from starlette.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from app.main import app
from app.config import API_KEY_NAME, API_KEY_VALUE


client = TestClient(app)


def test_images_resize_denied():
    response = client.post('/images/resize/')
    assert response.status_code == HTTP_401_UNAUTHORIZED
