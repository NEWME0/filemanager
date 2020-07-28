from PIL import Image, UnidentifiedImageError
from fs.errors import ResourceNotFound, DestinationExists
from contextlib import contextmanager
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.common.singleton import Singleton
from app.services.storage import storage, suppress_fs_exceptions


@contextmanager
def suppress_pillow_exceptions():
    try:
        yield
    except UnidentifiedImageError as exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(exception)
        )


class Redactor(Singleton):
    home = storage.home

    def resize(self, src_path, dst_path, width, height):
        """ Resize image at src_path and save to dst_path """
        with suppress_fs_exceptions():
            if not self.home.isfile(src_path):
                raise ResourceNotFound(src_path)
            if self.home.exists(dst_path):
                raise DestinationExists(dst_path)

        src_os_path = self.home.getospath(src_path).decode('utf-8')
        dst_os_path = self.home.getospath(dst_path).decode('utf-8')

        with suppress_pillow_exceptions():
            src_image = Image.open(src_os_path)
            dst_image = src_image.resize((width, height))
            dst_image.save(dst_os_path)

        return JSONResponse(dst_path)


redactor = Redactor()
