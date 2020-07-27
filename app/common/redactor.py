from fs.errors import ResourceNotFound, DestinationExists
from PIL import Image, UnidentifiedImageError

from starlette.responses import JSONResponse

from app.common.singleton import Singleton
from app.common.storage import storage, suppress_fs_exceptions


class Redactor(Singleton):
    home = storage.home

    def resize(self, src_path, dst_path, width, height):
        with suppress_fs_exceptions():
            if not self.home.isfile(src_path):
                raise ResourceNotFound(src_path)
            if self.home.exists(dst_path):
                raise DestinationExists(dst_path)

        src_os_path = self.home.getospath(src_path).decode('utf-8')
        dst_os_path = self.home.getospath(dst_path).decode('utf-8')

        try:
            im = Image.open(src_os_path)
        except UnidentifiedImageError:
            return False, 'Unidentified image type'

        resized_im = im.resize((width, height))
        resized_im.save(dst_os_path)

        return JSONResponse(dst_path)


redactor = Redactor()
