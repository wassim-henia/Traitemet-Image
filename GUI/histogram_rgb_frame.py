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


class HistogramRGBFrame(tk.Frame):

    def __init__(self, parent, image: np.ndarray):
        super().__init__(parent)
        self.image = image
        self.createWidgets()

    def createWidgets(self):

        img = self.image
        hist_red = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_green = cv2.calcHist([img], [1], None, [256], [0, 256])
        hist_blue = cv2.calcHist([img], [2], None, [256], [0, 256])

        fig, (ax) = plt.subplots(1, 1)
        fig.set_size_inches(5, 5)
        fig.set_facecolor('#3b3b3b')
        ax.set_facecolor('#3b3b3b')

        ax.plot(hist_red, color='r')
        ax.plot(hist_green, color='g')
        ax.plot(hist_blue, color='b')

        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('#3b3b3b')
        ax.spines['right'].set_color('#3b3b3b')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.title.set_color('white')

        ax.relim([0, 256])
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1)


# img = cv2.imread("./cat.jpg")

# root = tk.Tk()
# hc = HistogramRGBFrame(root, img)
# hc.pack(side="top")

# root.mainloop()
