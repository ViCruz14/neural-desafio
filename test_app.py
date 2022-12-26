import base64
import io

from PIL import Image
from tasks import resize_image


def test_resized_image_should_have_384_x_384():
    with open('test_image.png', 'rb') as img_file:
        img_str = base64.b64encode(img_file.read())
        resized = resize_image(img_str)

        pillow_obj = Image.open(io.BytesIO(base64.b64decode(resized)))

        assert pillow_obj.size == (384,384)