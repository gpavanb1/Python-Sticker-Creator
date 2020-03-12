from segment import Segment


def get_meme(inputString, text):
    seg = Segment(inputString, text)
    seg_map = seg.find_segments()
    return seg.vis_segmentation()


