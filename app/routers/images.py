from fastapi import APIRouter
from fastapi.param_functions import Query

from app.services.redactor import redactor


router = APIRouter(redirect_slashes=False)


@router.post('/resize/')
def resize_image(
        src_path: str = Query(..., max_length=255),
        dst_path: str = Query(..., max_length=255),
        height: int = Query(..., gt=0),
        width: int = Query(..., gt=0),
):
    return redactor.resize(src_path, dst_path, width, height)
