from segment import Segment

text = "YESONTI YESONTI PANLU CHESTHURU RA NAA PHOTO THONI"
seg = Segment("images/stock_example.jpg", text)
seg_map = seg.find_segments()
seg.vis_segmentation()
