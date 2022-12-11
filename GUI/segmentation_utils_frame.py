import random
from tkinter import *
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


def class_average(cl, start, end):
    niv = np.arange(start, end)
    return np.sum(cl * niv) / np.sum(cl)


def get_variance(hist, s):
    c0 = hist[:s]
    c1 = hist[s:]
    pc0 = np.sum(c0) / np.sum(hist)
    pc1 = np.sum(c1) / np.sum(hist)
    m = class_average(hist, 0, 255)
    m0 = class_average(c0, 0, s)
    m1 = class_average(c1, s, 255)
    return pc0 * (m0 - m) ** 2 + pc1 * (m1 - m) ** 2


def otsu_thresholding(hist):
    max_variance = 0
    seuil = 0
    for s in range(1, 254):
        variance = get_variance(hist, s)
        if variance > max_variance:
            max_variance = variance
            seuil = s
    return seuil


def extract_color_threshold(image: np.ndarray, threshold: int):
    return np.where(image < threshold, 255, 0)


def image_seuil_and(image: np.ndarray, r, g, b):
    red_channel, green_channel, blue_channel = image[:,
                                                     :, 2], image[:, :, 1], image[:, :, 0]
    image_seuil_red = extract_color_threshold(red_channel, r)
    image_seuil_green = extract_color_threshold(green_channel, g)
    image_seuil_blue = extract_color_threshold(blue_channel, b)
    result = np.bitwise_and(
        image_seuil_red, image_seuil_green, image_seuil_blue)
    return result.astype('uint8')


def image_seuil_or(image: np.ndarray, r, g, b):
    red_channel, green_channel, blue_channel = image[:,
                                                     :, 2], image[:, :, 1], image[:, :, 0]
    image_seuil_red = extract_color_threshold(red_channel, r)
    image_seuil_green = extract_color_threshold(green_channel, g)
    image_seuil_blue = extract_color_threshold(blue_channel, b)
    result = np.bitwise_or(
        image_seuil_red, image_seuil_green, image_seuil_blue)
    return result.astype('uint8')


class SegmentationUtilsFrame(Frame):

    kernel = np.ones((5, 5), np.uint8)

    def updateCanva(self):
        self.ax.imshow(self.transformed_image, cmap='gray', vmin=0, vmax=255)
        self.canvas.draw()

    def erosion(self,):
        self.transformed_image = cv2.erode(
            self.transformed_image, self.kernel, iterations=1)
        self.updateCanva()

    def dilatation(self):
        self.transformed_image = cv2.dilate(
            self.transformed_image, self.kernel, iterations=1)
        self.updateCanva()

    def fermeture(self):
        self.erosion()
        self.dilatation()
        self.updateCanva()

    def ouverture(self):
        self.dilatation()
        self.erosion()
        self.updateCanva()

    def set_otsu_value(self):
        img = self.image
        hist_red = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_green = cv2.calcHist([img], [1], None, [256], [0, 256])
        hist_blue = cv2.calcHist([img], [2], None, [256], [0, 256])
        otsu_red, otsu_green, otsu_blue = otsu_thresholding(
            hist_red), otsu_thresholding(hist_green), otsu_thresholding(hist_blue)

        self.r_slider.set(otsu_red)
        self.g_slider.set(otsu_green)
        self.b_slider.set(otsu_blue)
        self.update_plot()

    def update_plot(self):
        self.draw_binary_image(self.variable.get(), self.r_slider.get(),
                               self.g_slider.get(), self.b_slider.get())

    def update_r_slider(self, event):
        self.update_plot()

    def update_g_slider(self, event):
        self.update_plot()

    def update_b_slider(self, event):
        self.update_plot()

    def radio_checked(self):
        self.update_plot()

    def __init__(self, parent, image: np.ndarray):
        super().__init__(parent)
        self.b_slider = None
        self.g_slider = None
        self.r_slider = None
        self.variable = None
        self.image = image
        self.canvas = None
        self.transformed_image = None
        self.create_widgets()

    def init_plot(self):
        fig, (ax) = plt.subplots(1, 1)
        self.ax = ax
        fig.set_size_inches(4, 3)
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('#3b3b3b')
        ax.spines['right'].set_color('#3b3b3b')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.title.set_color('white')
        fig.set_facecolor('#3b3b3b')
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        self.canvas = canvas
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)

    def draw_binary_image(self, method: str, r: int, g: int, b: int):
        self.transformed_image = image_seuil_and(
            self.image, r, g, b) if method == "AND" else image_seuil_or(self.image, r, g, b)

        self.ax.imshow(self.transformed_image, cmap='gray', vmin=0, vmax=255)
        self.canvas.draw()
        return

    def create_widgets(self):
        self.configure(background="#3b3b3b")
        # otsu button
        otsu_frame = LabelFrame(self, borderwidth=0, bg="#3b3b3b")
        otsu_frame.grid(row=0, column=0)

        otsu_button = Button(otsu_frame, text='Otsu thresholds',
                             command=self.set_otsu_value)
        otsu_button.grid(row=0, column=0)

        # sliders
        self.r_slider = Scale(otsu_frame, from_=0, to=256, orient=HORIZONTAL)
        self.r_slider.grid(row=1, column=0)

        self.r_slider.bind("<ButtonRelease-1>", self.update_r_slider)

        self.g_slider = Scale(otsu_frame, from_=0, to=256, orient=HORIZONTAL)
        self.g_slider.grid(row=2, column=0)

        self.g_slider.bind("<ButtonRelease-1>", self.update_g_slider)

        self.b_slider = Scale(otsu_frame, from_=0, to=256, orient=HORIZONTAL)
        self.b_slider.grid(row=3, column=0)

        self.b_slider.bind("<ButtonRelease-1>", self.update_b_slider)

        switch_frame = LabelFrame(otsu_frame)
        switch_frame.grid(row=4, column=0)
        self.init_plot()

        self.variable = StringVar(None, "AND")

        AND_button = Radiobutton(switch_frame, text="AND", variable=self.variable,
                                 indicatoron=False, value="AND", width=8, command=self.radio_checked)
        OR_button = Radiobutton(switch_frame, text="OR", variable=self.variable,
                                indicatoron=False, value="OR", width=8, command=self.radio_checked)

        AND_button.grid(row=0, column=0)
        OR_button.grid(row=0, column=1)

        # Morphological operations
        morph_buttons = LabelFrame(self, borderwidth=0, bg="#3b3b3b")
        morph_buttons.grid(row=0, column=1)

        erosion = Button(morph_buttons, text='erosion', command=self.erosion)
        erosion.grid(row=0, column=1, pady=5)

        dilatation = Button(morph_buttons, text='dilatation',
                            command=self.dilatation)
        dilatation.grid(row=1, column=1, pady=5)

        ouverture = Button(morph_buttons, text='ouverture',
                           command=self.ouverture)
        ouverture.grid(row=2, column=1, pady=5)

        fermeture = Button(morph_buttons, text='fermeture',
                           command=self.fermeture)
        fermeture.grid(row=3, column=1, pady=5)

# def uploadFileCommand(self):
#     self.filename = fd.askopenfilename(
#         title='Open a file',
#         initialdir='~',
#         filetypes=self.filetypes)
#     self.show_image()

# def show_image(self):
#     self.image = cv2.imread(self.filename)[:, :, ::-1]
#     fig, (ax) = plt.subplots(1, 1)
#     fig.suptitle('Selected Image :')
#     fig.set_size_inches(5, 5)
#     ax.imshow(self.image)
#     canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
#     canvas.draw()
#     canvas.get_tk_widget().grid(row=2, column=1)


# root = tk.Tk()
# hc = SegmentationUtilsFrame(root)
# hc.pack(side="top")
#
# root.mainloop()
