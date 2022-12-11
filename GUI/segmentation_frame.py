from tkinter import *
from tkinter import ttk

from GUI.get_image_frame_seg import UploadFileSegFrame
from GUI.histogram_rgb_frame import HistogramRGBFrame
from GUI.segmentation_utils_frame import SegmentationUtilsFrame


class SegmentationFrame(ttk.Frame):
    def image_change_handler(self, image):
        print('image handler lauched')
        self.histogram = HistogramRGBFrame(
            self, image)
        self.histogram.grid(row=0, column=3)
        utils = SegmentationUtilsFrame(self, image)
        utils.grid(row=0, column=1)

    def __init__(self, root):
        super().__init__(root, width=1200, height=600)

        self.histogram = None
        image = UploadFileSegFrame(
            self,  image_change_handler=self.image_change_handler)
        image.grid(row=0, column=0)
