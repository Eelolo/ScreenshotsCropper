class ButtonsMenu:
    def __init__(self, main, cropping_area):
        self.main = main
        self.cropping_area = cropping_area
        self.canvas = self.cropping_area.canvas
        self.area = self.cropping_area.area
        self.area_coords = self.cropping_area.area_coords
        self.create_buttons()

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        return self.canvas.create_polygon(points, **kwargs, smooth=True)


    def create_buttons(self):
        center = int(self.area_coords[0] - (self.area_coords[0] - self.area_coords[2]) / 2)
        x0 = center - 110
        y0 = self.area_coords[5] - 50
        x1 = x0 + 100
        y1 = self.area_coords[5] - 25
        text_center_x = int(x0 - (x0 - x1) / 2)
        text_center_y = int(y0 - (y0 - y1) / 2)

        self.decline_btn = self.round_rectangle(x0, y0, x1, y1, radius=10, fill="gray", outline='black', width=2)
        self.decline_text = self.canvas.create_text(text_center_x, text_center_y, text='Decline', fill='white')

        x0 = center + 10
        y0 = self.area_coords[5] - 50
        x1 = x0 + 100
        y1 = self.area_coords[5] - 25
        text_center_x = int(x0 - (x0 - x1) / 2)
        text_center_y = int(y0 - (y0 - y1) / 2)

        self.accept_btn = self.round_rectangle(x0, y0, x1, y1, radius=10, fill="white", outline='black', width=2)
        self.accept_text = self.canvas.create_text(text_center_x, text_center_y, text='Accept', fill='black')
