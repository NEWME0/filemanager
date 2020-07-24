from fastapi import APIRouter, Security
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.settings import API_KEY_NAME, API_KEY_VALUE


get_api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
get_api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
get_api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(get_api_key_query),
    api_key_header: str = Security(get_api_key_header),
    api_key_cookie: str = Security(get_api_key_cookie),
):
    """ Try to found apikey in query, header or cookie """
    if api_key_query == API_KEY_VALUE:
        return api_key_query

    if api_key_header == API_KEY_VALUE:
        return api_key_header

    if api_key_cookie == API_KEY_VALUE:
        return api_key_cookie

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

# Init router
router = APIRouter()


@router.get('/')
async def set_cookie():
    """ Set apikey into cookies """
    response = JSONResponse('Cookie is set')
    response.set_cookie(key=API_KEY_NAME, value=API_KEY_VALUE)
    return response


@router.delete('/')
async def delete_cookie():
    """ Delete apikey from cookies """
    response = JSONResponse('Cookie is deleted')
    response.delete_cookie(key=API_KEY_NAME)
    return response
