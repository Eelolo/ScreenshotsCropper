from tkinter import *
from PIL import ImageGrab, ImageTk, Image
from pystray import MenuItem, Icon, Menu
import keyboard
import time
import math

class App(Frame):
    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)

        self.icon = None
        self.icon_img = Image.open("ico.png")

        self.configure_root()
        self.create_widgets()
        self.configure_widgets()
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
        left_coords = 0, height / 2 - 25, 5, height / 2 + 25
        right_coords = width, height / 2 - 25, width - 5, height / 2 + 25
        up_coords = width / 2 - 25, 0, width / 2 + 25, 5
        down_coords = width / 2 - 25, height, width / 2 + 25, height - 5
        upper_handle = self.canv.create_rectangle(
            up_coords[0],
            up_coords[1],
            up_coords[2],
            up_coords[3],
            fill='white',
            tag = 'upper_handle'

        )
        bottom_handle = self.canv.create_rectangle(
            down_coords[0],
            down_coords[1],
            down_coords[2],
            down_coords[3],
            fill='white',
            tag='bottom_handle'

        )
        left_handle = self.canv.create_rectangle(
            left_coords[0],
            left_coords[1],
            left_coords[2],
            left_coords[3],
            fill='white',
            tag='left_handle'

        )
        right_handle = self.canv.create_rectangle(
            right_coords[0],
            right_coords[1],
            right_coords[2],
            right_coords[3],
            fill='white',
            tag='right_handle'

        )
        self.canv.tag_bind(upper_handle, '<B1-Motion>', lambda event, tag='upper_handle': self.move_vert(event, tag))
        self.canv.tag_bind(upper_handle, "<ButtonPress-1>", lambda event, tag='upper_handle': self.move_start_vert(event, tag))

        self.canv.tag_bind(bottom_handle, '<B1-Motion>', lambda event, tag='bottom_handle': self.move_vert(event, tag))
        self.canv.tag_bind(bottom_handle, "<ButtonPress-1>", lambda event, tag='bottom_handle': self.move_start_vert(event, tag))

        self.canv.tag_bind(left_handle, '<B1-Motion>', lambda event, tag='left_handle': self.move_hor(event, tag))
        self.canv.tag_bind(left_handle, "<ButtonPress-1>", lambda event, tag='left_handle': self.move_start_hor(event, tag))

        self.canv.tag_bind(right_handle, '<B1-Motion>', lambda event, tag='right_handle': self.move_hor(event, tag))
        self.canv.tag_bind(right_handle, "<ButtonPress-1>", lambda event, tag='right_handle': self.move_start_hor(event, tag))

    def move_start_hor(self, event, tag):
        x, y, x1, y1 = self.canv.coords(tag)
        self.to_left_border = event.x - x
        self.to_right_border = x1 - event.x

    def move_hor(self, event, tag):
        x, y, x1, y1 = self.canv.coords(tag)
        self.canv.coords(tag, event.x-self.to_left_border, y, event.x+self.to_right_border, y1)
        self.update_handles_pos_gor()

    def move_start_vert(self, event, tag):
        x, y, x1, y1 = self.canv.coords(tag)
        self.to_upper_border = event.y - y
        self.to_bottom_border = y1 - event.y

    def move_vert(self, event, tag):
        x, y, x1, y1 = self.canv.coords(tag)
        self.canv.coords(tag, x, event.y-self.to_upper_border, x1, event.y+self.to_bottom_border)
        self.update_handles_pos_vert()

    def update_handles_pos_gor(self):
        lx, _, lx1, _ = self.canv.coords('left_handle')
        rx, _, rx1, _ = self.canv.coords('right_handle')

        _, uy, _, uy1 = self.canv.coords('upper_handle')
        _, by, _, by1 = self.canv.coords('bottom_handle')

        between_handles = rx - ((rx - lx1) / 2)

        self.canv.coords('upper_handle', between_handles - 25, uy, between_handles + 25, uy1)
        self.canv.coords('bottom_handle', between_handles - 25, by, between_handles + 25, by1)

    def update_handles_pos_vert(self):
        _, uy, _, uy1 = self.canv.coords('upper_handle')
        _, by, _, by1 = self.canv.coords('bottom_handle')

        lx, _, lx1, _ = self.canv.coords('left_handle')
        rx, _, rx1, _ = self.canv.coords('right_handle')

        between_handles = uy - ((uy - by1) / 2)

        self.canv.coords('left_handle', lx, between_handles - 25, lx1, between_handles + 25)
        self.canv.coords('right_handle', rx, between_handles - 25, rx1, between_handles + 25)

    def create_image(self):
        width = self.screenshot.width()
        height = self.screenshot.height()
        self.canv.configure(width=width, height=height)
        self.canv.create_image(0, 0, anchor='nw', image=self.screenshot, tag='screenshot')
        self.canv.pack()

    def update_image(self):
        if not self.canv.find_all():
            self.create_image()
        else:
            width = self.screenshot.width()
            height = self.screenshot.height()
            self.canv.configure(width=width, height=height)
            self.canv.itemconfigure('screenshot', image=self.screenshot)

    def withdraw_window(self):
        self.root.withdraw()
        menu = Menu(MenuItem('Show', self.show_window, default=True), MenuItem('Quit', self.quit_window))
        self.icon = Icon("ScreenshotsCutter", self.icon_img, "Screenshots\nCutter", menu)
        self.icon.run()

    def create_widgets(self):
        self.lbl = Label(self, text='There is no image here.\nUse the Print Screen button.')
        self.canv = Canvas(self)

    def configure_widgets(self):
        self.canv.bind("<Motion>", self.change_cursor)

    def draw_widgets(self):
        self.lbl.pack()

    def run(self):
        self.mainloop()

    def in_crop_area_check(self, event):
        uy1 = self.canv.coords('upper_handle')[3]
        by = self.canv.coords('bottom_handle')[1]
        lx1 = self.canv.coords('left_handle')[2]
        rx = self.canv.coords('right_handle')[0]

        if event.x > lx1 and event.x < rx and event.y > uy1 and event.y < by:
            return True

        return False

    def change_cursor(self, event):
        # cursors = ['fleur', 'sizing', 'sb_h_double_arrow', 'sb_v_double_arrow']
        if self.in_crop_area_check(event):
            self.canv.config(cursor='fleur')
        else:
            self.canv.config(cursor='arrow')

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
