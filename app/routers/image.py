from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from app.common.redactor import redactor


router = APIRouter()


@router.post('/resize')
def resize_image(src_path: str, dst_path: str, width: int, height: int):
    ok, result = redactor.resize(src_path, dst_path, width, height)
    code = HTTP_200_OK if ok else HTTP_400_BAD_REQUEST
    body = {'result': result} if ok else {'detail': result}
    return JSONResponse(body, status_code=code)
