import run_tf
import settings
import tensorflow as tf
import cv2
import io
import base64
import numpy as np
from matplotlib import gridspec
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patheffects as path_effects
import matplotlib
# make sure Tk backend is used
matplotlib.use("TkAgg")
from PIL import Image
from helper import img_string_to_cv2


def add_meme_text(_str, image):
    # Find location to add
    _width = image.shape[1]
    _height = image.shape[0]

    # Meme font
    prop = fm.FontProperties(fname='fonts/debussy.ttf')

    # Justify text
    text = plt.text(_width*0.5, _height*0.8, _str, color='blue', fontproperties=prop,
                    multialignment='center', wrap=True,
                    ha='center', va='center', size=20)
    text.set_path_effects([path_effects.Stroke(linewidth=6, foreground='white'),
                           path_effects.Normal()])


def make_transparent(src):
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(src)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 4)
    return dst


def smooth_edges(image):
    # Median blur - smooth edges
    img = cv2.medianBlur(image, 35)
    return img


def contour_mask(image, mask):
    # Get edges through Canny edge detection
    edged = cv2.Canny(mask, 30, 200)
    # Finding Contours
    contours, hierarchy = cv2.findContours(edged,
                          cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # Draw contours
    # -1 signifies drawing all contours
    cv2.drawContours(image, contours, -1, (255, 255, 255), 8)

    return image


def mask_out(src, mask):
    _mask_out = cv2.subtract(mask, src)
    _mask_out = cv2.subtract(mask, _mask_out)
    return _mask_out


class Segment:
    def __init__(self, image_string, meme_text, dpi=127.68):
        # Variables
        self.segment_map = None
        self.meme_text = meme_text
        self.dpi = dpi

        # Initialize TF model
        print("Using model: " + settings.model_file)
        self.interpreter = tf.lite.Interpreter(model_path=settings.model_file)
        self.interpreter.allocate_tensors()
        print("Loaded TF interpreter")

        # Load image
        # TODO : Add error capture
        self.image = img_string_to_cv2(image_string)
        print("Loaded image")

    def find_segments(self):
        output_tensors = run_tf.run_model(self.interpreter, self.image)
        self.segment_map = run_tf.output_to_classes(output_tensors)
        return self.segment_map

    # Code taken partially from Google Colab
    # https://github.com/tensorflow/models/blob/master/research/deeplab/deeplab_demo.ipynb
    def vis_segmentation(self):
        """Visualizes input image, segmentation map and overlay view."""
        # Current details
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB).astype(np.uint8)
        seg_map = self.segment_map

        plt.figure(figsize=(512/self.dpi, 512/self.dpi), dpi=self.dpi)
        grid_spec = gridspec.GridSpec(1, 1)

        # Process segmentation mask
        # Scale seg_map
        seg_map = (seg_map/np.max(seg_map)) * 255
        seg_image = Image.fromarray(seg_map.astype('uint8'))
        seg_image = cv2.cvtColor(np.array(seg_image), cv2.COLOR_RGB2BGR)

        # Resize segmentation mask
        _width = image.shape[1]
        _height = image.shape[0]
        _num_channels = 3
        res_seg_image = cv2.resize(seg_image, (_width, _height),
                                   _num_channels)

        # Postprocess mask
        res_seg_image = smooth_edges(res_seg_image)

        # Mask out image
        res_image = mask_out(image, res_seg_image)

        # Contour mask
        res_image = contour_mask(res_image, res_seg_image)

        # Add text
        plt.subplot(grid_spec[0])

        # Resize to standard 512x512 before display
        res_image = cv2.resize(res_image, (512, 512))
        add_meme_text(self.meme_text, res_image)

        # Make image transparent
        res_image = make_transparent(res_image)

        # Show image
        plt.imshow(res_image)
        plt.axis('off')

        # Convert to bytestring
        prefix = b'data:image/jpeg;base64,'
        buf = io.BytesIO()
        plt.savefig(buf, format='jpeg', transparent=True)
        buf.seek(0)
        image_string = (prefix + base64.b64encode(
        buf.getvalue())).decode("utf-8")
        return image_string
        # plt.show()

