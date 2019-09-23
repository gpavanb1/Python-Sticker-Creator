import run_tf
import settings
import tensorflow as tf
import cv2
import numpy as np
from matplotlib import gridspec
from matplotlib import pyplot as plt


LABEL_NAMES = np.asarray([
        'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
        'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
        'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
    ])


class Segment:
    def __init__(self, img_path):
        # Variables
        self.segment_map = None

        # Initialize TF model
        print("Using model: " + settings.model_file)
        self.interpreter = tf.lite.Interpreter(model_path=settings.model_file)
        self.interpreter.allocate_tensors()
        print("Loaded TF interpreter")

        # Load image
        # TODO : Add error capture
        self.image = cv2.imread(img_path)
        print("Loaded image")

        # Additional variables
        FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
        self.FULL_COLOR_MAP = self.label_to_color_image(FULL_LABEL_MAP)

    def find_segments(self):
        output_tensors = run_tf.run_model(self.interpreter, self.image)
        self.segment_map = run_tf.output_to_classes(output_tensors)
        return self.segment_map

    # Code taken from Google Colab
    # https://github.com/tensorflow/models/blob/master/research/deeplab/deeplab_demo.ipynb
    @staticmethod
    def create_pascal_label_colormap():
        """Creates a label colormap used in PASCAL VOC segmentation benchmark.

        Returns:
          A Colormap for visualizing segmentation results.
        """
        colormap = np.zeros((256, 3), dtype=int)
        ind = np.arange(256, dtype=int)

        for shift in reversed(range(8)):
            for channel in range(3):
                colormap[:, channel] |= ((ind >> channel) & 1) << shift
            ind >>= 3

        return colormap

    # Code taken from Google Colab
    # https://github.com/tensorflow/models/blob/master/research/deeplab/deeplab_demo.ipynb
    def label_to_color_image(self, label):
        """Adds color defined by the dataset colormap to the label.

        Args:
          label: A 2D array with integer type, storing the segmentation label.

        Returns:
          result: A 2D array with floating type. The element of the array
            is the color indexed by the corresponding element in the input label
            to the PASCAL color map.

        Raises:
          ValueError: If label is not of rank 2 or its value is larger than color
            map maximum entry.
        """
        if label.ndim != 2:
            raise ValueError('Expect 2-D input label')

        colormap = self.create_pascal_label_colormap()

        if np.max(label) >= len(colormap):
            raise ValueError('label value too large.')

        return colormap[label]

    # Code taken from Google Colab
    # https://github.com/tensorflow/models/blob/master/research/deeplab/deeplab_demo.ipynb
    def vis_segmentation(self):
        """Visualizes input image, segmentation map and overlay view."""
        # Current details
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB).astype(np.uint8)
        seg_map = self.segment_map

        plt.figure(figsize=(15, 5))
        grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

        plt.subplot(grid_spec[0])
        plt.imshow(image)
        plt.axis('off')
        plt.title('input image')

        plt.subplot(grid_spec[1])
        seg_image = self.label_to_color_image(seg_map).astype(np.uint8)
        # Blur seg_image
        seg_image = cv2.GaussianBlur(seg_image, (5, 5), 0)
        plt.imshow(seg_image)
        plt.axis('off')
        plt.title('segmentation map')

        plt.subplot(grid_spec[2])
        _width = image.shape[1]
        _height = image.shape[0]
        _num_channels = 3
        res_seg_image = cv2.resize(seg_image, (_width, _height), _num_channels)
        plt.imshow(image)
        plt.imshow(res_seg_image, alpha=0.7)
        plt.axis('off')
        plt.title('segmentation overlay')

        unique_labels = np.unique(seg_map)
        ax = plt.subplot(grid_spec[3])
        plt.imshow(
            self.FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
        ax.yaxis.tick_right()
        plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
        plt.xticks([], [])
        ax.tick_params(width=0.0)
        plt.grid('off')
        plt.show()


