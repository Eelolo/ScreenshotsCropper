from tkinter import *
from PIL import ImageGrab, ImageTk, Image
from pystray import MenuItem, Icon, Menu
import keyboard
import time


class App(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)

        self.icon = None
        self.icon_img = Image.open("ico.png")

        self.configure_root()
        self.create_widgets()
        self.draw_widgets()

    def configure_root(self):
        self.root.protocol('WM_DELETE_WINDOW', self.withdraw_window)

    def quit_window(self):
        self.icon.stop()
        self.root.destroy()

    def show_window(self):
        if self.icon:
            self.icon.stop()
            self.root.after(0, self.root.deiconify)
            self.icon = None

    def show_after_printscreen(self):
        self.show_window()
        self.lbl.pack_forget()
        time.sleep(0.1)
        self.grab_image()
        self.update_image()
        self.create_handles()

    def create_handles(self):
        width = self.screenshot.width()
        height = self.screenshot.height()
        left_coords = 0, height / 2 - 100, 20, height / 2 + 100
        right_coords = width, height / 2 - 100, width - 20, height / 2 + 100
        up_coords = width / 2 - 100, 0, width / 2 + 100, 20
        down_coords = width / 2 - 100, height, width / 2 + 100, height - 20
        upper_handle = self.canv.create_rectangle(
            up_coords[0],
            up_coords[1],
            up_coords[2],
            up_coords[3],
            fill='red',
            tag = 'up'

        )
        bottom_handle = self.canv.create_rectangle(
            down_coords[0],
            down_coords[1],
            down_coords[2],
            down_coords[3],
            fill='red'
        )
        left_handle = self.canv.create_rectangle(
            left_coords[0],
            left_coords[1],
            left_coords[2],
            left_coords[3],
            fill='red',
        )
        right_handle = self.canv.create_rectangle(
            right_coords[0],
            right_coords[1],
            right_coords[2],
            right_coords[3],
            fill='red'
        )

    def create_image(self):
        width = self.screenshot.width()
        height = self.screenshot.height()
        self.canv.configure(width=width, height=height)
        self.canv.create_image(0, 0, anchor='nw', image=self.screenshot)
        self.canv.pack()

    def update_image(self):
        if not self.canv.find_all():
            self.create_image()
        else:
            width = self.screenshot.width()
            height = self.screenshot.height()
            self.canv.configure(width=width, height=height)
            self.canv.itemconfigure(self.canv.find_all()[-1], image=self.screenshot)

    def withdraw_window(self):
        self.root.withdraw()
        menu = Menu(MenuItem('Show', self.show_window, default=True), MenuItem('Quit', self.quit_window))
        self.icon = Icon("ScreenshotsCutter", self.icon_img, "Screenshots\nCutter", menu)
        self.icon.run()

    def create_widgets(self):
        self.lbl = Label(self, text='There is no image here.\nUse the Print Screen button.')
        self.canv = Canvas(self)

    def draw_widgets(self):
        self.lbl.pack()

    def run(self):
        self.mainloop()

    def proportional_resize(self, image, new_height=800, new_width=None):
        width, height = image.size

        if not new_width:
            new_width = int((width * new_height) / height)
        else:
            new_height = int((height * new_width) / width)

        image = image.resize((new_width, new_height))

        return image

    def grab_image(self):
        self.screenshot = ImageGrab.grabclipboard()
        height = int(self.screenshot.size[0]/2.5)
        self.screenshot = self.proportional_resize(self.screenshot, new_height=height)
        self.screenshot = ImageTk.PhotoImage(self.screenshot)


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    app.pack()
    keyboard.add_hotkey('Print Screen', app.show_after_printscreen)
    app.run()
