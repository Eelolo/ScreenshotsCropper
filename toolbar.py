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

        self.dark_bg = rgb_to_tk_color((32, 34, 37))
        self.light_bg = rgb_to_tk_color((54, 57, 63))

        self.create_widgets()
        self.draw_widgets()

    def create_widgets(self):
        self.canvas = Canvas(self, width=1365, height=100, bg=self.dark_bg, highlightthickness=0, bd=0)

        points = get_round_rect_points(10, 10, 1355, 90, radius=25)
        self.canvas.create_polygon(points, fill=self.light_bg, smooth=True)

    def draw_widgets(self):
        self.canvas.pack()
