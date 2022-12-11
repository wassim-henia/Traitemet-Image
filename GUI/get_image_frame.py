import random
import tkinter
import tkinter as tk
from tkinter import Button, filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure


def rand_helper(i):
    a = random.randint(0, 20)
    if a == 20:
        return 255
    elif a == 0:
        return 0
    else:
        return i


class UploadFileFrame(tk.Frame):
    filetypes = (
        ('jpgs', '*.jpg'),
        ('pngs', '*.png'),
        ('pgms', '*.pgm'),
        ('ppms', '*.ppm'),
    )

    def __init__(self, parent, image_change_hanlder):
        super().__init__(parent)
        self.createWidgets()
        self.filename = ""
        self.image_change_hanlder = image_change_hanlder

    def createWidgets(self):
        self.configure(background="#3b3b3b")
        self.uploadFileButton = tk.Button(
            self, text='Upload Image', bg='#585858', fg='white', command=self.uploadFileCommand)

        self.uploadFileButton.grid(row=1, column=1)

    def uploadFileCommand(self):
        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='~',
            filetypes=self.filetypes)
        self.show_image()

    def show_image(self):
        if "pgm" in self.filename:
            with open(self.filename, 'rb') as pgmf:
                self.image = plt.imread(pgmf)
        else: 
            self.image = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)
        fig, (ax) = plt.subplots(1, 1)
        self.ax = ax
        fig.set_size_inches(6, 4)
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('#3b3b3b')
        ax.spines['right'].set_color('#3b3b3b')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.title.set_color('white')

        ax.imshow(self.image, cmap='gray', vmin=0, vmax=255)
        fig.set_facecolor('#3b3b3b')
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        self.canvas = canvas
        canvas.get_tk_widget().grid(row=2, column=1)
        self.image_change_hanlder(self.image)

    def set_image(self, newimg: np.ndarray):
        self.image = newimg.astype("uint8")
        self.ax.imshow(newimg, cmap='gray', vmin=0, vmax=255)
        self.canvas.draw()
        self.image_change_hanlder(self.image)

    def linear_transform(self):
        img = self.image
        lin_img = (img - img.min()) / (img.max() - img.min())
        lin_img = lin_img * 255
        self.set_image(lin_img)
    
    def apply_map(self, map, data):
        tmp = []
        for line in data:
            tmp.append([map[i] for i in line])
        return tmp
    
    def histogram(self, data):
        freq_arr = [0] * 256
        for line in data:
            for i in line:
                freq_arr[i] += 1
        return freq_arr
    
    def cumul_histogram(self, data):
        hist = self.histogram(data)
        tmp = 0
        ret = []
        for i in hist:
            tmp += i
            ret.append(tmp)
        return ret
    
    def equalization_array(self):
        cumul = self.cumul_histogram(self.image)
        prob_cumul = (i / (self.image.shape[0] * self.image.shape[1]) for i in cumul)
        cumul_eg = (i * 255 for i in prob_cumul)
        map = [int(i) for i in cumul_eg]
        self.set_image(np.array(self.apply_map(map, self.image)))
    
    def par_morceaux_linear(self,x1_entry,y1_entry,x2_entry,y2_entry):
        point1 = [int(x1_entry.get()), int(y1_entry.get())]
        point2 = [int(x2_entry.get()), int(y2_entry.get())]
        map = []
        for i in range(point1[0] + 1):
            rate = point1[1] / point1[0]
            map.append(int(rate * i))

        for i in range(point1[0] + 1, point2[0] + 1):
            rate = (point2[1] - point1[1]) / (point2[0] - point1[0])
            offset = point2[1] - rate * point2[0]
            map.append(int(rate * i + offset))
        point3 = (255, 255)

        for i in range(point2[0] + 1, point3[0] + 1):
            rate = (point3[1] - point2[1]) / (point3[0] - point2[0])
            offset = point3[1] - rate * point3[0]
            map.append(int(rate * i + offset))

        self.set_image(np.array(self.apply_map(map, self.image)))

    def equalize(self):
        equ = cv2.equalizeHist(self.image)
        self.set_image(equ)

    def apply_noise(self):
        flat_noisy_image = np.array([rand_helper(i)
                                     for i in self.image.flatten()])
        a = flat_noisy_image.reshape(self.image.shape)
        self.set_image(a)

    def mean_filter(self, n=3):
        image = self.image
        filtered = image.copy()
        w = n//2
        for i in range(w, image.shape[0] - w):
            for j in range(w, image.shape[1] - w):
                block = image[i - w:i + w + 1, j - w:j + w + 1]
                mean_result = np.mean(block, dtype=np.float32)
                filtered[i][j] = int(mean_result)
        self.set_image(filtered)

    def median_filter(self, n=3):
        image = self.image
        filtered = image.copy()
        w = n//2
        for i in range(w, image.shape[0]-w):
            for j in range(w, image.shape[1]-w):
                block: np.ndarray = image[i-w:i+w+1, j-w:j+w+1]
                flat_sorted_block = np.sort(block.flatten())
                median_value = flat_sorted_block[((n**2)//2)+1]
                filtered[i][j] = int(median_value)
        self.set_image(filtered)
    
    def high_filter(self, n):
        image = self.image
        filtered = image.copy()
        w = n//2
        for i in range(w,image.shape[0]-w):
            for j in range(w,image.shape[1]-w):
                block = image[i-w:i+w+1, j-w:j+w+1]
                mean_result = np.mean(block,dtype=np.float32)
                filtered[i][j] = filtered[i][j]-int(mean_result)
        self.set_image(filtered)

