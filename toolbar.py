from tkinter import *
from PIL import Image, ImageTk
from functions.functions import rgb_to_tk_color, get_round_rect_points


class ToolBar(Frame):
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

        self.create_widgets()
        self.draw_widgets()

    def create_widgets(self):
        self.canvas = Canvas(self, width=1365, height=100, bg=self.dark_bg, highlightthickness=0, bd=0)

        points = get_round_rect_points(10, 10, 1355, 90, radius=25)
        self.canvas.create_polygon(points, fill=self.light_bg, smooth=True)

        self.left_frame = Frame(self)
        self.right_frame = Frame(self)
        self.canvas.create_window(25, 25, anchor='nw', window=self.left_frame)
        self.canvas.create_window(1190, 25, anchor='nw', window=self.right_frame)

        self.crop_btn = Button(
            self.left_frame, image=self.crop_img, height=50, width=50,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )
        self.text_btn = Button(
            self.left_frame, image=self.text_img, height=50, width=50,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )
        self.arrow_btn = Button(
            self.left_frame, image=self.arrow_img, height=50, width=50,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )
        self.line_btn = Button(
            self.left_frame, image=self.line_img, height=50, width=50,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )

        self.clipboard_btn = Button(
            self.right_frame, image=self.clipboard_img, height=50, width=50,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0
        )
        self.diskette_btn = Button(
            self.right_frame, image=self.diskette_img, height=50, width=50,
            relief='flat', bg=self.light_bg, activebackground=self.light_bg, bd=0, command=self.main.withdraw_window
        )

    def draw_widgets(self):
        self.canvas.pack()
        self.crop_btn.pack(side='left', ipadx=10)
        self.text_btn.pack(side='left', ipadx=10)
        self.arrow_btn.pack(side='left', ipadx=10)
        self.line_btn.pack(side='left', ipadx=10)
        self.diskette_btn.pack(side='right', ipadx=10)
        self.clipboard_btn.pack(side='right', ipadx=10)
