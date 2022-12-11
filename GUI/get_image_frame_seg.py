import random
import tkinter
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure


class UploadFileSegFrame(tk.Frame):

    filetypes = (
        ('jpgs', '*.jpg'),
        ('pngs', '*.png'),
        ('pgms', '*.pgm'),
        ('ppms', '*.ppm'),
    )

    def __init__(self, parent, image_change_handler):
        super().__init__(parent)
        self.createWidgets()
        self.image_change_handler = image_change_handler
        self.filename = ""

    def createWidgets(self):
        self.configure(background="#3b3b3b")
        self.uploadFileButton = tk.Button(
            self, text='Upload Image', command=self.uploadFileCommand, bg='#585858', fg='white',)

        self.uploadFileButton.grid(row=0, column=0)

    def uploadFileCommand(self):
        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='~',
            filetypes=self.filetypes)
        self.show_image()

    def show_image(self):
        self.image = cv2.imread(self.filename)
        fig, (ax) = plt.subplots(1, 1)
        fig.set_facecolor('#3b3b3b')
        ax.set_facecolor('#3b3b3b')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('#3b3b3b')
        ax.spines['right'].set_color('#3b3b3b')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.title.set_color('white')

        fig.set_size_inches(4, 4)
        ax.imshow(self.image[:, :, ::-1])
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        self.image_change_handler(self.image)


# root = tk.Tk()
# hc = UploadFileSegFrame(root)
# hc.pack(side="top")

# root.mainloop()
