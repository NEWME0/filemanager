from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.exceptions import HTTPException
from app.common.redactor import redactor


router = APIRouter()


@router.post('/resize')
def resize_image(
        src_path: str = Query(..., max_length=255),
        dst_path: str = Query(..., max_length=255),
        height: int = Query(..., gt=0),
        width: int = Query(..., gt=0),
):
    """ Resize image specified by src_path and save at dst_path """
    ok, result = redactor.resize(src_path, dst_path, width, height)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return JSONResponse(result, status_code=HTTP_200_OK)
