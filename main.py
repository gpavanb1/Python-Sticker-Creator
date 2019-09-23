from segment import Segment

seg = Segment("images/stock_example.jpg")
seg_map = seg.find_segments()
seg.vis_segmentation()
