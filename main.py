from tkinter import *


class App(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)

    def create_widgets(self):
        self.image_canv = Canvas(self)

    def draw_widgets(self):
        self.image_canv.pack()

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    app.run()