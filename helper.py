import base64
import cv2
import numpy as np


def img_string_to_cv2(image_string):
    jpg_original = base64.b64decode(image_string[23:])
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img_cv2 = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)

    return img_cv2

    