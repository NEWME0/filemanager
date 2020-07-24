import os
import requests
import mimetypes
from fs import open_fs
from fs.errors import *
from requests.exceptions import *
from fastapi import UploadFile
from app.settings import HOME_DIR
from app.common.singleton import Singleton
from app.common.models import EntryInfo


ALLOWED_CONTENT_TYPES = [
    'image/png',
    'image/jpeg',
]


class Storage(Singleton):
    home = open_fs(HOME_DIR)

    async def browse_dir(self, path):
        """ Browse folder """
        try:
            result = self.home.scandir(path, namespaces=['details'])
        except (
            IllegalBackReference,
            ResourceNotFound,
            DirectoryExpected,
        ) as exception:
            return False, str(exception)

        result = [EntryInfo.from_storage(info).dict() for info in result]

        return True, result

    async def create_dir(self, path):
        """ Create directory """
        try:
            self.home.makedirs(path)
        except (
            IllegalBackReference,
            DirectoryExists,
            DirectoryExpected,
        ) as exception:
            return False, str(exception)

        return True, path

    async def update_dir(self, src_path, dst_path, copy=False, merge=False):
        """ Move, copy or merge folders """
        try:
            if merge is False and self.home.exists(dst_path):
                raise DestinationExists(dst_path)

            if copy:
                self.home.copydir(src_path, dst_path, create=True)
            else:
                self.home.movedir(src_path, dst_path, create=True)
        except (
            IllegalBackReference,
            ResourceNotFound,
            DirectoryExpected,
            DestinationExists,
        ) as exception:
            return False, str(exception)

        return True, dst_path

    async def delete_dir(self, path):
        """ Delete folder """
        try:
            self.home.removedir(path)
        except (
            IllegalBackReference,
            RemoveRootError,
            ResourceNotFound,
            DirectoryExpected,
        ) as exception:
            return False, str(exception)

        return True, os.path.dirname(path)

    async def browse_file(self, path):
        """ Return file """
        try:
            if not self.home.isfile(path):
                raise FileExpected(path)
        except (
            IllegalBackReference,
            ResourceNotFound,
            FileExpected,
        ) as exception:
            return False, str(exception)

        path = self.home.getospath(path).decode('utf-8')
        filename = os.path.basename(path)
        media_type, encoding = mimetypes.guess_type(path, strict=True)

        result = {
            'path': path,
            'filename': filename,
            'media_type': media_type,
        }

        return True, result

    async def create_file(self, src_file: UploadFile, src_link: str, dst_path: str):
        if not self.home.isdir(dst_path):
            return False, 'Directory expected'

        if src_file is not None:
            if src_file.content_type not in ALLOWED_CONTENT_TYPES:
                return False, 'Content type {src_file.content_type} not allowed'

            path = os.path.join(dst_path, src_file.filename)

            try:
                self.home.create(path, wipe=False)
            except (
                IllegalBackReference,
                ResourceNotFound,
                DestinationExists,
            ) as exception:
                return False, str(exception)

            self.home.writebytes(path, await src_file.read())

            return True, path

        if src_link is not None:
            try:
                response = requests.get(src_link, stream=True)
            except (
                HTTPError,
                ConnectionError,
                ConnectTimeout,
            ) as exception:
                return False, str(exception)

            if response.headers.get('content-type') not in ALLOWED_CONTENT_TYPES:
                return False, 'Content type {src_file.content_type} not allowed'

            filename = os.path.basename(src_link)
            path = os.path.join(dst_path, filename)

            try:
                if self.home.isfile(path):
                    raise DestinationExists(path)

                self.home.create(path, wipe=False)
            except (
                IllegalBackReference,
                ResourceNotFound,
                DestinationExists,
            ) as exception:
                return False, str(exception)

            self.home.upload(path, response.raw)

            return True, path

        return False, 'Source not provided'

    async def update_file(self, src_path, dst_path, copy=False, overwrite=False):
        """ Move or copy file """
        try:
            if copy:
                self.home.copy(src_path, dst_path, overwrite=overwrite)
            else:
                self.home.move(src_path, dst_path, overwrite=overwrite)
        except (
            IllegalBackReference,
            ResourceNotFound,
            FileExpected,
            DestinationExists,
        ) as exception:
            return False, str(exception)

        return True, dst_path

    async def delete_file(self, path):
        """ Delete file """
        try:
            self.home.remove(path)
        except (
            IllegalBackReference,
            ResourceNotFound,
            FileExpected,
        ) as exception:
            return False, str(exception)

        return True, os.path.dirname(path)


storage = Storage()
