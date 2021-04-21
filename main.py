from tkinter import *
from PIL import ImageGrab, ImageTk


class App(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)

        self.create_widgets()
        self.draw_widgets()
        self.grab_image()

    def create_widgets(self):
        self.image_canv = Canvas(self, width=1920, height=1080)

    def draw_widgets(self):
        self.image_canv.pack()

    def run(self):
        self.mainloop()

    def grab_image(self):
        self.screenshot = ImageTk.PhotoImage(ImageGrab.grabclipboard())

if __name__ == '__main__':
    root = Tk()
    app = App(root)
    app.pack()
    app.run()