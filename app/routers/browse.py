from fastapi import APIRouter, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.datastructures import UploadFile
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app.common.storage import storage


router = APIRouter()


@router.get('/')
async def browse_dir(path: str = ''):
    ok, result = storage.browse_dir(path)
    code = HTTP_200_OK if ok else HTTP_400_BAD_REQUEST
    body = {'result': result} if ok else {'detail': result}
    return JSONResponse(body, status_code=code)


@router.post('/')
async def create_dir(path: str = ''):
    ok, result = storage.create_dir(path)
    code = HTTP_200_OK if ok else HTTP_400_BAD_REQUEST
    body = {'result': result} if ok else {'detail': result}
    return JSONResponse(body, status_code=code)


@router.put('/')
async def update_dir(src_path: str, dst_path: str, copy: bool = False, merge: bool = False):
    ok, result = storage.update_dir(src_path, dst_path, copy, merge)
    code = HTTP_200_OK if ok else HTTP_400_BAD_REQUEST
    body = {'result': result} if ok else {'detail': result}
    return JSONResponse(body, status_code=code)


@router.delete('/')
async def delete_dir(path: str = ''):
    ok, result = storage.delete_dir(path)
    code = HTTP_200_OK if ok else HTTP_400_BAD_REQUEST
    body = {'result': result} if ok else {'detail': result}
    return JSONResponse(body, status_code=code)


@router.get('/download')
async def download_file(path: str):
    ok, result = storage.download_file(path)

    if not ok:
        return JSONResponse(result, status_code=HTTP_400_BAD_REQUEST)

    name, path, mime = result.values()
    return FileResponse(filename=name, path=path, media_type=mime)


@router.post('/upload')
async def upload_file(path: str, file: UploadFile = File(...)):
    data = await file.read()
    ok, result = storage.upload_file(path, file, data)
    code = HTTP_200_OK if ok else HTTP_400_BAD_REQUEST
    body = {'result': result} if ok else {'detail': result}
    return JSONResponse(body, status_code=code)


@router.post('/upload-url')
async def upload_url_file(path: str, url: str):
    ok, result = storage.upload_url(path, url)
    code = HTTP_200_OK if ok else HTTP_400_BAD_REQUEST
    body = {'result': result} if ok else {'detail': result}
    return JSONResponse(body, status_code=code)
