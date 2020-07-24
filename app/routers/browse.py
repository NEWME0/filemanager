from typing import Union, Optional
from fastapi import APIRouter, File, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.datastructures import UploadFile
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.exceptions import HTTPException

from app.common.storage import storage


router = APIRouter()


@router.get('/')
async def browse_dir(path: str = Query('/', max_length=255)):
    """ Return entries info of specified folder """
    ok, result = await storage.browse_dir(path)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return JSONResponse(result, status_code=HTTP_200_OK)


@router.post('/')
async def create_dir(path: str = Query(..., max_length=255)):
    """ Create new folder """
    ok, result = await storage.create_dir(path)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return JSONResponse(result, status_code=HTTP_200_OK)


@router.patch('/')
async def update_dir(
    src_path: str = Query(..., max_length=255),
    dst_path: str = Query(..., max_length=255),
    copy: bool = False,
    merge: bool = False,
):
    """ Move, copy or merge existing folders """
    ok, result = await storage.update_dir(src_path, dst_path, copy, merge)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return JSONResponse(result, status_code=HTTP_200_OK)


@router.delete('/')
async def delete_dir(path: str = Query(..., max_length=255)):
    """ Delete existing folder """
    ok, result = await storage.delete_dir(path)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return JSONResponse(result, status_code=HTTP_200_OK)


@router.get('/file')
async def browse_file(path: str = Query(..., max_length=255)):
    """ Return file """
    ok, result = await storage.browse_file(path)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return FileResponse(**result)


@router.post('/file')
async def create_file(
    src_file: Optional[UploadFile] = File(None),
    src_link: Optional[str] = Query(None, max_length=255),
    dst_path: str = Query(..., max_length=255),
):
    """ Upload file directly of by url """
    ok, result = await storage.create_file(src_file, src_link, dst_path)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return JSONResponse(result, status_code=HTTP_200_OK)


@router.patch('/file')
async def update_file(
    src_path: str = Query(..., max_length=255),
    dst_path: str = Query(..., max_length=255),
    copy: bool = False,
    overwrite: bool = False,
):
    """ Move or copy file """
    ok, result = await storage.update_file(src_path, dst_path, copy, overwrite)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return JSONResponse(result, status_code=HTTP_200_OK)


@router.delete('/file')
async def delete_file(path: str = Query(..., max_length=255)):
    """ Delete existing file """
    ok, result = await storage.delete_file(path)
    if not ok:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=result)
    return JSONResponse(result, status_code=HTTP_200_OK)
