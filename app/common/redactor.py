from PIL import Image, UnidentifiedImageError
from app.common.singleton import Singleton
from app.common.storage import storage


class Redactor(Singleton):
    home = storage.home

    def resize(self, src_path, dst_path, width, height):
        if not self.home.isfile(src_path):
            return False, f'Resource {src_path} not found'

        if self.home.exists(dst_path):
            return False, f'Destination {dst_path} exists'

        src_os_path = self.home.getospath(src_path).decode('utf-8')
        dst_os_path = self.home.getospath(dst_path).decode('utf-8')

        try:
            im = Image.open(src_os_path)
        except UnidentifiedImageError:
            return False, 'Unidentified image type'

        resized_im = im.resize((width, height))
        resized_im.save(dst_os_path)

        return True, dst_path


redactor = Redactor()
