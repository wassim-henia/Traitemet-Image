from tkinter import *
from tkinter import ttk

from GUI.overview_frame import OverviewFrame
from GUI.segmentation_frame import SegmentationFrame


if __name__ == '__main__':
    root = Tk()
    root.title('Image Processor')
    root.geometry("1200x600")

    s = ttk.Style()

    s.configure('TFrame', background='#3b3b3b')

    tabs = ttk.Notebook(root)
    tabs.pack()

    overview = OverviewFrame(tabs)
    overview.pack(fill='both', expand=1)

    segmentation = SegmentationFrame(tabs)
    segmentation.pack(fill='both', expand=1)

    tabs.add(overview, text='overview')
    tabs.add(segmentation, text='segmentation')

    root.mainloop()
