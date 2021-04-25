from tkinter import *
from PIL import ImageGrab, ImageTk, Image
from pystray import MenuItem, Icon, Menu
import keyboard
import time
from cropping_area import Cropping_area


class App(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)

        self.icon = None
        self.icon_img = Image.open("ico.png")

        self.configure_root()
        self.create_widgets()
        # self.configure_widgets()
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
        self.cropping_area = Cropping_area(self)

    def create_image(self):
        self.img_canv.configure(width=self.width, height=self.height)
        self.img_canv.create_image(0, 0, anchor='nw', image=self.screenshot_tk, tag='screenshot')
        self.img_canv.pack()

    def update_image(self):
        if not self.img_canv.find_all():
            self.create_image()
        else:
            self.img_canv.configure(width=self.width, height=self.height)
            self.img_canv.itemconfigure('screenshot', image=self.screenshot_tk)

    def withdraw_window(self):
        self.root.withdraw()
        menu = Menu(MenuItem('Show', self.show_window, default=True), MenuItem('Quit', self.quit_window))
        self.icon = Icon("ScreenshotsCutter", self.icon_img, "Screenshots\nCutter", menu)
        self.icon.run()

    def create_widgets(self):
        self.lbl = Label(self, text='There is no image here.\nUse the Print Screen button.')
        self.img_canv = Canvas(self, borderwidth=0, highlightthickness=0)

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
        new_height = int(self.screenshot.size[0]/2.5)
        self.screenshot = self.proportional_resize(self.screenshot, new_height=new_height)
        self.width, self.height = self.screenshot.size
        self.screenshot_tk = ImageTk.PhotoImage(self.screenshot)

if __name__ == '__main__':
    root = Tk()
    app = App(root)
    app.pack()
    keyboard.add_hotkey('Print Screen', app.show_after_printscreen)
    app.run()
