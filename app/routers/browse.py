from typing import Optional
from fastapi import APIRouter, File, Query
from fastapi.datastructures import UploadFile

from app.common.storage import storage


router = APIRouter()


@router.get('/')
async def browse_dir(
    path: str = Query('/', max_length=255)
):
    return await storage.browse_dir(path)


@router.post('/')
async def create_dir(
    path: str = Query(..., max_length=255)
):
    return await storage.create_dir(path)


@router.patch('/')
async def update_dir(
    src_path: str = Query(..., max_length=255),
    dst_path: str = Query(..., max_length=255),
    copy: bool = False,
    merge: bool = False
):
    return await storage.update_dir(src_path, dst_path, copy, merge)


@router.delete('/')
async def delete_dir(
    path: str = Query(..., max_length=255)
):
    return await storage.delete_dir(path)


@router.get('/file')
async def browse_file(
    path: str = Query(..., max_length=255)
):
    return await storage.browse_file(path)


@router.post('/file')
async def create_file(
    src_file: Optional[UploadFile] = File(None),
    src_link: Optional[str] = Query(None, max_length=255),
    dst_path: str = Query(..., max_length=255)
):
    return await storage.create_file(src_file, src_link, dst_path)


@router.patch('/file')
async def update_file(
    src_path: str = Query(..., max_length=255),
    dst_path: str = Query(..., max_length=255),
    copy: bool = False,
    overwrite: bool = False
):
    return await storage.update_file(src_path, dst_path, copy, overwrite)


@router.delete('/file')
async def delete_file(
    path: str = Query(..., max_length=255)
):
    return await storage.delete_file(path)
