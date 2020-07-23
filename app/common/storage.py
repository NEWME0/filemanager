import os
import requests
import mimetypes
from fs import open_fs
from fs.errors import *
from app.settings import HOME_DIR
from app.common.singleton import Singleton


ALLOWED_MEDIA_TYPES = [
    'image/png',
    'image/jpeg',
]


class Storage(Singleton):
    home = open_fs(HOME_DIR)

    def browse_dir(self, path):
        try:
            result = self.home.listdir(path)

        except ResourceNotFound:
            return False, f'Resource not found'

        except IllegalBackReference:
            return False, f'Illegal back reference'

        except DirectoryExpected:
            return False, f'Directory expected'

        else:
            return True, result

    def create_dir(self, path):
        try:
            self.home.makedirs(path)

        except DirectoryExists:
            return False, 'Directory exists'

        except DirectoryExpected:
            return False, 'Directory expected'

        except IllegalBackReference:
            return False, 'Illegal back reference'

        else:
            return True, path

    def update_dir(self, src_path, dst_path, copy=False, merge=False):
        try:
            if merge is False:
                if self.home.isdir(dst_path):
                    raise DirectoryExists(dst_path)

                if self.home.exists(dst_path):
                    raise DirectoryExpected(dst_path)

            if copy:
                self.home.copydir(src_path, dst_path, create=True)
            else:
                self.home.movedir(src_path, dst_path, create=True)

        except ResourceNotFound:
            return False, 'Resource not found'

        except DirectoryExists:
            return False, 'Directory exists'

        except DirectoryExpected:
            return False, 'Directory expected'

        else:
            return True, dst_path

    def delete_dir(self, path):
        try:
            self.home.removedir(path)

        except ResourceNotFound:
            return False, 'Resource not found'

        except DirectoryExpected:
            return False, 'Directory expected'

        except RemoveRootError:
            return False, 'Remove root are not allowed'

        return True, path

    def upload_file(self, path, file, data):
        if self.home.isdir(path):
            path = os.path.join(path, file.filename)

        try:
            if self.home.exists(path):
                raise DestinationExists(path)

            self.home.create(path)
            self.home.writebytes(path, data)

        except DestinationExists:
            return False, 'Destination exists'

        return True, path

    def upload_url(self, path, url):
        mime, encoding = mimetypes.guess_type(url, strict=True)

        if mime not in ALLOWED_MEDIA_TYPES:
            return False, f'Media type {mime} not allowed'

        name = os.path.basename(url)

        if self.home.isdir(path):
            path = os.path.join(path, name)

        if self.home.exists(path):
            return False, "File exists"

        try:
            response = requests.get(url, stream=True)

        except requests.exceptions.HTTPError:
            return False, 'HTTP bad url'

        if response.status_code != 200:
            return False, 'Not found'

        try:
            self.home.upload(path, file=response.raw)

        except ResourceNotFound:
            return False, 'Resource not found'

        except DestinationExists:
            return False, 'Destination exists'

        return True, path

    def download_file(self, path):
        try:
            info = self.home.getdetails(path)

            if not info.is_file:
                raise FileExpected(path)

        except ResourceNotFound:
            return False, 'Resource not found'

        except FileExpected:
            return False, 'File expected'

        name = info.name
        mime = 'application/octet-stream'
        path = self.home.getospath(path)

        return True, {'name': name, 'path': path, 'mime': mime}


storage = Storage()
