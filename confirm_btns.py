class ButtonsMenu:
    def __init__(self, main, cropping_area):
        self.main = main
        self.cropping_area = cropping_area
        self.canvas = self.cropping_area.canvas

        self.btn_width = 100
        self.btn_height = 25
        self.btn_pad_x = 8
        self.btn_pad_y = 25

        self.create_buttons()
        self.configure_widgets()

    def configure_widgets(self):
        self.canvas.bind('<B1-Motion>', self.update_btns_pos, '+')

    def get_round_rect_points(self, x1, y1, x2, y2, radius=10):
        points = [
            x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1,
            x2, y1, x2, y1 + radius, x2, y1 + radius, x2, y2 - radius,
            x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2,
            x1 + radius, y2, x1 + radius, y2, x1, y2, x1, y2 - radius,
            x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1
        ]

        return points

    def get_accept_btn_angles(self):
        left_angle = self.cropping_area.area_coords[0]
        right_angle = self.cropping_area.area_coords[2]
        lower_angle = self.cropping_area.area_coords[5]
        area_width = self.cropping_area.area[0]
        img_height = self.cropping_area.height

        center = int(left_angle - (left_angle - right_angle) / 2)

        if area_width > self.btn_width * 2 + self.btn_pad_x * 6:
            x0 = center + self.btn_pad_x
            x1 = x0 + self.btn_width
            y1 = lower_angle - self.btn_pad_y
            y0 = y1 - self.btn_height

            if lower_angle < img_height - self.btn_pad_y * 2 - self.btn_height:
                y0 = lower_angle + self.btn_pad_y
                y1 = y0 + self.btn_height

        else:
            x0 = center - self.btn_width / 2
            x1 = x0 + self.btn_width
            y0 = lower_angle - self.btn_height * 2 - self.btn_pad_y - self.btn_pad_x
            y1 = y0 + self.btn_height

            if lower_angle < img_height - self.btn_height * 2 - self.btn_pad_y * 2 - self.btn_pad_x:
                y0 = lower_angle + self.btn_pad_y
                y1 = y0 + self.btn_height

        return x0, y0, x1, y1

    def get_decline_btn_angles(self):
        left_angle = self.cropping_area.area_coords[0]
        right_angle = self.cropping_area.area_coords[2]
        lower_angle = self.cropping_area.area_coords[5]
        area_width = self.cropping_area.area[0]
        img_height = self.cropping_area.height

        center = int(left_angle - (left_angle - right_angle) / 2)

        if area_width > self.btn_width * 2 + self.btn_pad_x * 6:
            x0 = center - self.btn_pad_x - self.btn_width
            x1 = x0 + self.btn_width
            y1 = lower_angle - self.btn_pad_y
            y0 = y1 - self.btn_height

            if lower_angle < img_height - self.btn_pad_y * 2 - self.btn_height:
                y0 = lower_angle + self.btn_pad_y
                y1 = y0 + self.btn_height

        else:
            x0 = center - 50
            y0 = lower_angle - 50
            x1 = x0 + 100
            y1 = lower_angle - 25

            if lower_angle < img_height - self.btn_height * 2 - self.btn_pad_y * 2 - self.btn_pad_x:
                y0 = lower_angle + 60
                y1 = lower_angle + 85

        return x0, y0, x1, y1

    def get_text_pos(self, x0, y0, x1, y1):
        x = int(x0 - (x0 - x1) / 2)
        y = int(y0 - (y0 - y1) / 2)

        return x, y

    def create_buttons(self):
        x0, y0, x1, y1 = self.get_decline_btn_angles()

        points = self.get_round_rect_points(x0, y0, x1, y1, radius=10)
        self.canvas.create_polygon(
            points, smooth=True, fill="gray", outline='black', width=2, tags=('ButtonsMenu', 'decline_btn')
        )
        point = self.get_text_pos(x0, y0, x1, y1)
        self.canvas.create_text(
            point, text='Decline', fill='white', tags=('ButtonsMenu', 'decline_text')
        )

        x0, y0, x1, y1 = self.get_accept_btn_angles()

        points = self.get_round_rect_points(x0, y0, x1, y1, radius=10)
        self.canvas.create_polygon(
            points, smooth=True, fill="white", outline='black', width=2, tags=('ButtonsMenu', 'accept_btn')
        )
        point = self.get_text_pos(x0, y0, x1, y1)
        self.canvas.create_text(
            point, text='Accept', fill='black', tags=('ButtonsMenu', 'accept_text')
        )

    def update_btns_pos(self, event):
        x0, y0, x1, y1 = self.get_decline_btn_angles()

        points = self.get_round_rect_points(x0, y0, x1, y1)
        self.canvas.coords('decline_btn', points)

        point = self.get_text_pos(x0, y0, x1, y1)
        self.canvas.coords('decline_text', point)

        x0, y0, x1, y1 = self.get_accept_btn_angles()

        points = self.get_round_rect_points(x0, y0, x1, y1)
        self.canvas.coords('accept_btn', points)

        point = self.get_text_pos(x0, y0, x1, y1)
        self.canvas.coords('accept_text', point)
