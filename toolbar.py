from tkinter import *
from PIL import Image, ImageTk


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
