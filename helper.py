import base64
from io import BytesIO
from PIL import Image


def b64_to_file(image_string, filename='sample.png'):
    img = Image.open(BytesIO(base64.b64decode(image_string[22:])))
    img.save(filename)

def file_to_b64(filename='test.png'):
    prefix = b'data:image/png;base64,'
    pil_img = Image.open(filename)
    buff = BytesIO()
    pil_img.save(buff, format="png")
    image_string = (prefix + base64.b64encode(
        buff.getvalue())).decode("utf-8")
    return image_string
    