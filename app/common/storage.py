from contextlib import contextmanager

import fs
from fs.errors import FSError, FileExpected, DirectoryExpected, DestinationExists
import requests
from requests.exceptions import RequestException, BaseHTTPError

from fastapi.datastructures import UploadFile
from starlette.responses import JSONResponse, FileResponse
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.settings import HOME_DIR, ALLOWED_CONTENT_TYPES
from app.common.singleton import Singleton
from app.common.models import EntryInfo


@contextmanager
def suppress_fs_exceptions():
    """ Replace all fs errors with HTTP_400_BAD_REQUEST """
    try:
        yield
    except FSError as exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(exception)
        )


@contextmanager
def suppress_requests_exceptions():
    """ Replace all requests errors with HTTP_400_BAD_REQUEST """
    try:
        yield
    except (RequestException, BaseHTTPError) as exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(exception)
        )


class Storage(Singleton):
    home = fs.open_fs(HOME_DIR)

    async def browse_dir(self, path):
        """ List folder containment info """
        with suppress_fs_exceptions():
            result = self.home.scandir(path, namespaces=['details'])
        result = [EntryInfo.from_storage(info).dict() for info in result]
        return JSONResponse(result)

    async def create_dir(self, path):
        """ Create directory """
        with suppress_fs_exceptions():
            self.home.makedirs(path)
        return JSONResponse(path)

    async def update_dir(self, src_path, dst_path, copy=False, merge=False):
        """ Move, copy or merge folders """
        with suppress_fs_exceptions():
            if merge is False and self.home.exists(dst_path):
                raise DestinationExists(dst_path)
            if copy:
                self.home.copydir(src_path, dst_path, create=True)
            else:
                self.home.movedir(src_path, dst_path, create=True)
        return JSONResponse(dst_path)

    async def delete_dir(self, path):
        """ Delete folder """
        with suppress_fs_exceptions():
            self.home.removedir(path)
        return JSONResponse(fs.path.dirname(path))

    async def browse_file(self, path):
        """ Download file """
        with suppress_fs_exceptions():
            if not self.home.isfile(path):
                raise FileExpected(path)
        path = self.home.getospath(path).decode('utf-8')
        return FileResponse(path)

    async def create_file(self, src_file: UploadFile, src_link: str, dst_path: str):
        """ Upload file directly or through url """
        # Check that dst_path are valid and pointing to a folder
        with suppress_fs_exceptions():
            if not self.home.isdir(dst_path):
                raise DirectoryExpected(dst_path)

        if src_file is not None:
            if src_file.content_type not in ALLOWED_CONTENT_TYPES:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f'Content type {src_file.content_type} not allowed'
                )
            path = fs.path.join(dst_path, src_file.filename)
            with suppress_fs_exceptions():
                self.home.create(path, wipe=False)
                self.home.writebytes(path, await src_file.read())
            return JSONResponse(path)

        if src_link is not None:
            # Request file by url
            with suppress_requests_exceptions():
                src_file = requests.get(src_link, stream=True)

            # Check content type
            if src_file.headers.get('content-type') not in ALLOWED_CONTENT_TYPES:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f'Content type {src_file.headers.get("content-type")} not allowed'
                )

            # Get file name from url
            name = fs.path.basename(src_link)
            # Make destination path
            path = fs.path.join(dst_path, name)

            # Create file
            with suppress_fs_exceptions():
                if self.home.isfile(path):
                    raise DestinationExists(path)
                self.home.create(path, wipe=False)
                self.home.upload(path, src_file.raw)

            return JSONResponse(path)

        # If src_file and src_link are both None raise HTTP_400_BAD_REQUEST
        return HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Source not provided'
        )

    async def update_file(self, src_path, dst_path, copy=False, overwrite=False):
        """ Move or copy file """
        with suppress_fs_exceptions():
            if copy:
                self.home.copy(src_path, dst_path, overwrite=overwrite)
            else:
                self.home.move(src_path, dst_path, overwrite=overwrite)
        return JSONResponse(dst_path)

    async def delete_file(self, path):
        """ Delete file """
        with suppress_fs_exceptions():
            self.home.remove(path)
        return JSONResponse(fs.path.dirname(path))


storage = Storage()
