from segment import Segment
from helper import b64_to_file, file_to_b64


def get_meme(inputString, text):
    b64_to_file(inputString)
    seg = Segment('sample.png', text)
    seg_map = seg.find_segments()
    return seg.vis_segmentation()


