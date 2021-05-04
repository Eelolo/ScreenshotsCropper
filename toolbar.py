from tkinter import *
from PIL import Image, ImageTk
from functions.functions import get_round_rect_points


class ToolBar(Frame):
    BTN_W = 50

    def __init__(self, main):
        self.main = main
        Frame.__init__(self, main)

        self.crop_img = ImageTk.PhotoImage(Image.open('icons/crop.png'))
        self.arrow_img = ImageTk.PhotoImage(Image.open('icons/arrow2.png'))
        self.diskette_img = ImageTk.PhotoImage(Image.open('icons/diskette.png'))
        self.line_img = ImageTk.PhotoImage(Image.open('icons/line1.png'))
        self.text_img = ImageTk.PhotoImage(Image.open('icons/text.png'))
        self.clipboard_img = ImageTk.PhotoImage(Image.open('icons/clipboard.png'))

        self.dark_bg = self.main.dark_bg
        self.light_bg = self.main.light_bg

        self.width = self.main.width
        self.height = self.BTN_W * 2
        self.pad = self.main.content_pad

        self.create_widgets()
        self.configure_widgets()
        self.draw_widgets()

    def configure_widgets(self):
        width = self.main.root.winfo_width()
        height = self.main.root.winfo_height() + self.height - self.pad
        x = (self.main.root.winfo_screenwidth() // 2) - (width // 2)

        self.main.root.geometry(f'{width}x{height}+{x}+{0}')
        self.main.bg_canv.configure(height=height)

    def create_widgets(self):
        self.canvas = Canvas(
            self, width=self.width, height=self.height, bg=self.dark_bg, highlightthickness=0, bd=0
        )

        x0, y0, x1, y1 = 0, self.pad, self.width, self.height - self.pad
        points = get_round_rect_points(x0, y0, x1, y1, radius=25)
        self.canvas.create_polygon(points, fill=self.light_bg, smooth=True)

        self.left_frame = Frame(self)
        self.right_frame = Frame(self)

        self.canvas.create_window(0, self.BTN_W / 2, anchor='nw', window=self.left_frame)
        self.canvas.create_window(self.width, self.BTN_W / 2, anchor='ne', window=self.right_frame)


        self.crop_btn = Button(
            self.left_frame, image=self.crop_img,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )
        self.text_btn = Button(
            self.left_frame, image=self.text_img,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )
        self.arrow_btn = Button(
            self.left_frame, image=self.arrow_img,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )
        self.line_btn = Button(
            self.left_frame, image=self.line_img,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )

        self.clipboard_btn = Button(
            self.right_frame, image=self.clipboard_img,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )
        self.diskette_btn = Button(
            self.right_frame, image=self.diskette_img,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )

    def draw_widgets(self):
        self.canvas.pack()
        self.crop_btn.pack(side='left', ipadx=10)
        self.text_btn.pack(side='left', ipadx=10)
        self.arrow_btn.pack(side='left', ipadx=10)
        self.line_btn.pack(side='left', ipadx=10)
        self.diskette_btn.pack(side='right', ipadx=10)
        self.clipboard_btn.pack(side='right', ipadx=10)
