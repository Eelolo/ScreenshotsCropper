from tkinter import *
from PIL import ImageGrab, ImageTk, Image
from pystray import MenuItem, Icon, Menu
import keyboard
import time
from cropping_area import CroppingArea
from toolbar import ToolBar
from functions.functions import proportional_resize, rgb_to_tk_color, get_round_rect_points, get_center_pos


class WelcomeWindow(Frame):
    WIDTH = 300
    HEIGHT = 200

    def __init__(self, root):
        self.root = root
        Frame.__init__(self, root)

        self.dark_bg = rgb_to_tk_color((32, 34, 37))
        self.light_bg = rgb_to_tk_color((54, 57, 63))
        self.close_icon = ImageTk.PhotoImage(Image.open('icons/close.png'))
        self.icon_white = ImageTk.PhotoImage(Image.open("icons/ico_white.png"))

        self.top_panel_h = 50
        self.top_panel_inner_pad = 5
        self.content_pad = 15

        self.welcome_text = 'There is no image here.\n\nUse the Print Screen button.'
        self.icons_gray = rgb_to_tk_color((200, 200, 200))

        self.icon = None
        self.icon_img = Image.open("icons/ico.png")

        self.configure_root()
        self.create_widgets()
        self.draw_widgets()

    def configure_root(self):
        self.root.protocol('WM_DELETE_WINDOW', self.withdraw_window)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", 1)
        self.root.resizable(False, False)
        self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}')

        self.center_window()

        self.root.bind('<Button-1>', self.root_move_start)
        self.root.bind('<B1-Motion>', self.root_move)

    def create_widgets(self):
        # self.lbl = Label(self, text='There is no image here.\nUse the Print Screen button.')
        # self.bg_canv = Canvas(self, bg=self.dark_bg, highlightthickness=0, bd=0)
        # self.img_frame = Frame(self)
        # self.img_canv = Canvas(self.img_frame, borderwidth=0, highlightthickness=0)

        self.bg_canv = Canvas(self, bg=self.dark_bg, highlightthickness=0, bd=0)

        x0 = self.content_pad
        y0 = self.content_pad + self.top_panel_h
        x1 = self.WIDTH - self.content_pad
        y1 = self.HEIGHT - self.content_pad
        points = get_round_rect_points(x0, y0, x1, y1, radius=25)
        self.bg_canv.create_polygon(points, fill=self.light_bg, smooth=True)

        self.close_btn = Button(
            self, command=self.withdraw_window, fg='white',
            activeforeground='red', image=self.close_icon,
            relief='flat', bg=self.light_bg, activebackground='red', bd=0
        )

        x = self.WIDTH - self.content_pad
        y = 0
        self.bg_canv.create_window(x, y, anchor='ne', window=self.close_btn)

        x = self.content_pad + self.icon_white.width() + self.top_panel_inner_pad
        x1 = self.WIDTH - self.content_pad
        y = self.icon_white.height()
        self.bg_canv.create_line(x, y, x1, y, fill=self.light_bg, width=3)

        x = self.content_pad
        y = self.top_panel_inner_pad
        self.bg_canv.create_image(x, y, anchor='nw', image=self.icon_white)

        x = self.WIDTH / 2
        y = self.top_panel_h / 2.5
        self.bg_canv.create_text(x, y, text='ScreenShotsCropper', fill='white', font=12)

        x, y = get_center_pos(0, self.top_panel_h, self.WIDTH, self.HEIGHT)
        self.bg_canv.create_text(x, y, text=self.welcome_text, fill=self.icons_gray, font=12)

    def draw_widgets(self):
        self.bg_canv.pack()

    def quit_window(self):
        self.icon.stop()
        self.root.destroy()

    def show_window(self):
        if self.icon:
            self.icon.stop()
            self.root.after(0, self.root.deiconify)
            self.icon = None

    def withdraw_window(self, event=None):
        self.root.withdraw()
        menu = Menu(MenuItem('Show', self.show_window, default=True), MenuItem('Quit', self.quit_window))
        self.icon = Icon("ScreenshotsCutter", self.icon_img, "Screenshots\nCropper", menu)
        self.icon.run()

    def run(self):
        self.mainloop()

    def root_move_start(self, event):
        self.root.diff_x = event.x
        self.root.diff_y = event.y

    def root_move(self, event):
        if str(event.widget) == f'.{self.winfo_name()}.!canvas':
            x = self.root.winfo_pointerx() - self.root.diff_x
            y = self.root.winfo_pointery() - self.root.diff_y
            self.root.geometry(f'+{x}+{y}')

    def center_window(self):
        x = (self.root.winfo_screenwidth() // 2) - (self.WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.HEIGHT // 2)

        self.root.geometry(f'+{x}+{y}')

# class App(Frame):
#     def __init__(self, root):
#         self.root = root
#         Frame.__init__(self, root)
#
#         self.top_panel_h = 50
#         self.content_pad = 15
#
#         self.icon_white = ImageTk.PhotoImage(Image.open("icons/ico_white.png"))
#
#         self.create_widgets()
#         self.draw_widgets()
#
#     def show_after_printscreen(self):
#         self.show_window()
#         self.lbl.pack_forget()
#         time.sleep(0.1)
#         self.grab_image()
#         self.update_image()
#
#         width = self.width + self.content_pad * 2
#         height = self.height + self.top_panel_h + self.content_pad
#         self.root.geometry(f'{width}x{height}')
#
#         self.bg_canv.configure(width=self.width + self.content_pad * 2, height=self.height + self.top_panel_h + self.content_pad)
#         self.bg_canv.pack()
#         self.bg_canv.create_window(self.content_pad, self.top_panel_h, anchor='nw', window=self.img_frame)
#         self.img_canv.pack()
#         self.upper_frame = Frame(self, width=self.width+self.content_pad * 2, height=self.top_panel_h, bg='red')
#         self.close_btn = Button(
#             self.upper_frame, command=self.withdraw_window, fg='white',
#             activeforeground='red', image=self.close_icon,
#             relief='flat', bg=self.light_bg, activebackground='red', bd=0
#         )
#         self.close_btn.pack(side='right')
#
#         self.bg_canv.create_window(self.width-self.content_pad, 0, anchor='nw', window=self.upper_frame)
#         self.bg_canv.create_line(70, 40, self.root.winfo_width() - 15, 40, fill=self.light_bg, width=3)
#         self.bg_canv.create_image(20, 5, anchor='nw', image=self.icon_white)
#
#         x = self.root.winfo_width() / 2
#         self.bg_canv.create_text(x, 20, text='ScreenShotsCropper', fill='white', font=12)
#
#         self.create_cropping_area()
#         self.create_toolbar()
#
#     def create_cropping_area(self):
#         if hasattr(self, 'cropping_area'):
#             self.cropping_area.delete_cropping_area()
#             del self.cropping_area
#
#         self.cropping_area = CroppingArea(self)
#
#     def create_toolbar(self):
#         if not hasattr(self, 'toolbar'):
#             self.toolbar = ToolBar(self)
#             self.bg_canv.create_window(15, 768 + 50, anchor='nw', window=self.toolbar)
#
#     def create_image(self):
#         self.img_canv.configure(width=self.width, height=self.height)
#         self.img_canv.create_image(0, 0, anchor='nw', image=self.screenshot_tk, tag='screenshot')
#
#     def update_image(self):
#         if not self.img_canv.find_all():
#             self.create_image()
#         else:
#             self.img_canv.configure(width=self.width, height=self.height)
#             self.img_canv.itemconfigure('screenshot', image=self.screenshot_tk)
#
#     def grab_image(self):
#         self.screenshot = ImageGrab.grabclipboard()
#         new_height = int(self.screenshot.size[0]/2.5)
#         self.screenshot = proportional_resize(self.screenshot, new_height=new_height)
#         self.width, self.height = self.screenshot.size
#         self.screenshot_tk = ImageTk.PhotoImage(self.screenshot)


if __name__ == '__main__':
    root = Tk()
    welcome_window = WelcomeWindow(root)
    welcome_window.pack()
    keyboard.add_hotkey('Print Screen', welcome_window.show_window)
    welcome_window.run()
