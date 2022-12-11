import random
import tkinter
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo

import cv2
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure


class HistogramFrame(tk.Frame):

    def __init__(self, parent, image: np.ndarray):
        super().__init__(parent)
        self.image = image
        self.createWidgets()

    @staticmethod
    def get_histogram(image: np.ndarray):
        histogram = []
        flattened_image = image.flatten()
        for i in range(0, 256):
            histogram.append(np.count_nonzero(flattened_image == i))
        return np.array(histogram)

    def createWidgets(self):
        fig, (ax) = plt.subplots(1, 1)
        fig.set_size_inches(6, 4)
        fig.set_facecolor('#3b3b3b')
        ax.set_facecolor('#3b3b3b')

        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('#3b3b3b')
        ax.spines['right'].set_color('#3b3b3b')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.xaxis.label.set_color('white')

        histogram = self.get_histogram(self.image)
        ax.plot(range(256), histogram)
        plt.tight_layout(pad=2)
        ax.set(xlabel='Niveau de gris', title="Histogram")
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1)

