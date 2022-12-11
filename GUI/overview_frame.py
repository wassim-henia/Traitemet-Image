from tkinter import *
from tkinter import ttk

from GUI.get_image_frame import UploadFileFrame
from GUI.histogram_frame import HistogramFrame
from GUI.statistics import StatisticsFrame


class OverviewFrame(ttk.Frame):
    options = ['choose filter', 'median', 'moyenne', "haut"]

    def validate(self, p):
        if str.isdigit(p) or p == "":
            return True
        else:
            return False

    def select_filter(self, event):
        if self.variable.get() != self.options[0]:
            self.dimension.configure(state='normal')

    def filter(self):
        if self.variable.get() == self.options[1]:
            self.image.median_filter(int(self.dimension.get()))
        elif self.variable.get() == self.options[2]:
            self.image.mean_filter(int(self.dimension.get()))
        elif self.variable.get() == self.options[3]:
            self.image.high_filter(int(self.dimension.get()))

    def equalize(self):
        self.image.equalization_array()

    def linear_transform(self):
        self.image.linear_transform()
    
    def par_morceaux_linear(self,root):
        window = Toplevel(root)
        window.geometry("200x200")
        point1 = Label(window,text="Point 1")
        x1_entry = Entry(window)
        y1_entry = Entry(window)

        point2 = Label(window,text="Point 2")
        x2_entry = Entry(window)
        y2_entry = Entry(window)

        confirm_button = Button(window,text='Confirmer', bg='#828282', fg='white', command=lambda: self.image.par_morceaux_linear(
            x1_entry,y1_entry,x2_entry,y2_entry
            ),
                              padx=20)
        point1.pack()
        x1_entry.pack()
        y1_entry.pack()
        point2.pack()
        x2_entry.pack()
        y2_entry.pack()
        confirm_button.pack()
        
    def apply_noise(self):
        self.image.apply_noise()

    def image_change_hanlder(self, image):
        print('image handler lauched')
        self.histogram = HistogramFrame(
            self.body, image)
        self.histogram.grid(row=0, column=1)
        self.footer = StatisticsFrame(self.body, image)
        self.grid_propagate(False)
        self.footer.grid(row=2)

    def __init__(self, root):
        super().__init__(root, width=1200, height=600)

        self.histogram = None
        self.footer = None
        header = LabelFrame(self, font=('Raleway', 25),
                            width=1200, height=100, bg='#317498')
        header.grid_propagate(False)
        header.grid(row=0)

        # contrast section
        contrast_frame = LabelFrame(
            header, borderwidth=0, bg='#317498', padx=10)
        contrast_frame.grid(row=0, column=0)

        contrast = Label(contrast_frame, text='Contrast',
                         fg='white', bg='#317498', pady=5)
        contrast.grid(row=0, sticky=W)

        equ_button = Button(contrast_frame, text='Egalisation',
                            bg='#828282', fg='white', command=self.equalize, padx=20)
        equ_button.grid(row=1, pady=5, sticky=W)

        lin_button = Button(contrast_frame, text='Tranformation Lineaire par morceau', bg='#828282', fg='white',
                            command=lambda: self.par_morceaux_linear(root))
        lin_button.grid(row=3)
        

        # filters section
        filters_frame = LabelFrame(
            header, borderwidth=0, bg='#317498', padx=50)
        filters_frame.grid(row=0, column=1)

        filters = Label(filters_frame, text='Filters',
                        fg='white', bg='#317498', pady=5)
        filters.grid(row=0, sticky=W)

        type_frame = LabelFrame(filters_frame, bg='#317498', borderwidth=0)
        type_frame.grid(row=1)

        type_text = Label(type_frame, text='Type:', fg='white', bg='#317498')
        type_text.grid(row=0, column=0)

        self.variable = StringVar(type_frame)
        self.variable.set(self.options[0])

        drop_down = OptionMenu(type_frame, self.variable,
                               *self.options, command=self.select_filter)
        drop_down.grid(row=0, column=1)

        dimension_frame = LabelFrame(
            filters_frame, borderwidth=0, bg='#317498')
        dimension_frame.grid(row=2, pady=5, sticky=W)

        dimension_text = Label(
            dimension_frame, text='Dim:', fg='white', bg='#317498')
        dimension_text.grid(row=1, column=0)

        space = Label(dimension_frame, text='', fg='white', bg='#317498')
        space.grid(row=1, column=1)

        vcmd = (self.register(self.validate))

        self.dimension = Entry(dimension_frame, width=10, state='disabled', validate='all',
                               validatecommand=(vcmd, '%P'))
        self.dimension.grid(row=1, column=2)

        space1 = Label(dimension_frame, text='', fg='white', bg='#317498')
        space1.grid(row=1, column=3)

        filter_button = Button(dimension_frame, text='Go',
                               bg='#828282', fg='white', command=self.filter)
        filter_button.grid(row=1, column=4)

        # noise section
        noise_frame = LabelFrame(header, borderwidth=0, bg='#317498')
        noise_frame.grid(row=0, column=3, sticky=E)

        noise = Label(noise_frame, text='Noise',
                      fg='white', bg='#317498', pady=5)
        noise.grid(row=0, sticky=W)

        noise_button = Button(noise_frame, text='Appliquer Bruit', bg='#828282', fg='white', command=self.apply_noise,
                              padx=20)
        noise_button.grid(row=1, sticky=W)

        self.body = LabelFrame(self, font=('Raleway', 25), width=1200,
                               height=500, bg='#3b3b3b', borderwidth=0)
        self.body.grid_propagate(False)
        self.body.grid(row=2)

        self.image = UploadFileFrame(
            self.body, image_change_hanlder=self.image_change_hanlder)
        self.image.grid(row=0, column=0)
