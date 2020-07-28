from typing import Optional
from fastapi import APIRouter
from fastapi.param_functions import Security, Query, Header, Cookie
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.config import API_KEY_NAME, API_KEY_VALUE


# Api key getters
get_api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
get_api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
get_api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(get_api_key_query),
    api_key_header: str = Security(get_api_key_header),
    api_key_cookie: str = Security(get_api_key_cookie),
):
    """
    Try to find api key in request's query, header or cookie
    Validate access or return HTTP_401_UNAUTHORIZED
    """
    if api_key_query == API_KEY_VALUE:
        return api_key_query

    if api_key_header == API_KEY_VALUE:
        return api_key_header

    if api_key_cookie == API_KEY_VALUE:
        return api_key_cookie

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )


# Init router
router = APIRouter(redirect_slashes=False)


@router.get('/')
async def set_cookie():
    """ Set api key into cookies """
    response = JSONResponse(f'API key has been set into cookie as {API_KEY_NAME}')
    response.set_cookie(key=API_KEY_NAME, value=API_KEY_VALUE)
    return response


@router.delete('/')
async def delete_cookie():
    """ Delete api key from cookies """
    response = JSONResponse(f'Cookie {API_KEY_NAME} has been deleted')
    response.delete_cookie(key=API_KEY_NAME)
    return response
