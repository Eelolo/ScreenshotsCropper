class Cropping_area:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.create_handles()

    def create_handles(self):
        width = self.width
        height = self.height

        left_coords = 0, height / 2 - 25, 5, height / 2 + 25
        right_coords = width, height / 2 - 25, width - 5, height / 2 + 25
        up_coords = width / 2 - 25, 0, width / 2 + 25, 5
        down_coords = width / 2 - 25, height, width / 2 + 25, height - 5

        upper_left = 0, 0, 0, 50, 5, 50, 5, 5, 50, 5, 50, 0
        lower_left = 0, height, 0, height-50, 5, height-50, 5, height-5,  50, height-5, 50, height

        upper_right = width, 0, width-50, 0, width-50, 5, width-5, 5, width-5, 50, width, 50
        lower_right = (
            width, height, width-50, height, width-50, height-5, width-5, height-5, width-5,
            height-50, width, height-50
        )

        upper_handle = self.canvas.create_rectangle(
            up_coords,
            fill='white',
            tag = 'upper_handle'

        )
        lower_handle = self.canvas.create_rectangle(
            down_coords,
            fill='white',
            tag='lower_handle'

        )
        left_handle = self.canvas.create_rectangle(
            left_coords,
            fill='white',
            tag='left_handle'

        )
        right_handle = self.canvas.create_rectangle(
            right_coords,
            fill='white',
            tag='right_handle'
        )
        upper_left_handle = self.canvas.create_polygon(
            upper_left,
            fill='white',
            tag='upper_left_handle',
            outline='black'
        )
        lower_left_handle = self.canvas.create_polygon(
            lower_left,
            fill='white',
            tag='lower_left_handle',
            outline='black'
        )
        upper_right_handle = self.canvas.create_polygon(
            upper_right,
            fill='white',
            tag='upper_right_handle',
            outline='black'
        )
        lower_right_handle = self.canvas.create_polygon(
            lower_right,
            fill='white',
            tag='lower_right_handle',
            outline='black'
        )

        self.canvas.tag_bind(upper_handle, '<B1-Motion>', lambda event, tag='upper_handle': self.move_vert(event, tag))
        self.canvas.tag_bind(upper_handle, "<ButtonPress-1>", lambda event, tag='upper_handle': self.move_start_vert(event, tag))

        self.canvas.tag_bind(lower_handle, '<B1-Motion>', lambda event, tag='lower_handle': self.move_vert(event, tag))
        self.canvas.tag_bind(lower_handle, "<ButtonPress-1>", lambda event, tag='lower_handle': self.move_start_vert(event, tag))

        self.canvas.tag_bind(left_handle, '<B1-Motion>', lambda event, tag='left_handle': self.move_hor(event, tag))
        self.canvas.tag_bind(left_handle, "<ButtonPress-1>", lambda event, tag='left_handle': self.move_start_hor(event, tag))

        self.canvas.tag_bind(right_handle, '<B1-Motion>', lambda event, tag='right_handle': self.move_hor(event, tag))
        self.canvas.tag_bind(right_handle, "<ButtonPress-1>", lambda event, tag='right_handle': self.move_start_hor(event, tag))

    def move_start_hor(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.to_left_border = event.x - x
        self.to_right_border = x1 - event.x

    def move_hor(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.canvas.coords(tag, event.x-self.to_left_border, y, event.x+self.to_right_border, y1)

        self.angle_handles_update_hor(tag)
        self.update_handles_pos_hor()


    def move_start_vert(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.to_upper_border = event.y - y
        self.to_lower_border = y1 - event.y
        self.event = event

    def get_angle_handle_tags(self, handle_tag):
        if handle_tag == 'upper_handle':
            return 'upper_left_handle', 'upper_right_handle'
        elif handle_tag == 'lower_handle':
            return 'lower_left_handle', 'lower_right_handle'
        elif handle_tag == 'left_handle':
            return 'upper_left_handle', 'lower_left_handle'
        elif handle_tag == 'right_handle':
            return 'upper_right_handle', 'lower_right_handle'
        else:
            return None

    def angle_handles_update_hor(self, handle_tag):
        upper_handle, lower_handle = self.get_angle_handle_tags(handle_tag)

        x = self.canvas.coords(handle_tag)[0]

        x0,y0, x1,y1, x2,y2, x3,y3, x4,y4, x5,y5 = self.canvas.coords(upper_handle)
        self.canvas.coords(upper_handle, x,y0, x,y1, x+5,y2, x+5,y3, x+50,y4, x+50,y5)

        x0,y0, x1,y1, x2,y2, x3,y3, x4,y4, x5,y5 = self.canvas.coords(lower_handle)
        self.canvas.coords(lower_handle, x,y0, x,y1, x+5,y2, x+5,y3, x+50,y4, x+50,y5)

    def move_vert(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.canvas.coords(tag, x, event.y-self.to_upper_border, x1, event.y+self.to_lower_border)
        self.update_handles_pos_vert()

    def update_handles_pos_hor(self):
        lx, _, lx1, _ = self.canvas.coords('left_handle')
        rx, _, rx1, _ = self.canvas.coords('right_handle')

        _, uy, _, uy1 = self.canvas.coords('upper_handle')
        _, loy, _, loy1 = self.canvas.coords('lower_handle')

        between_handles = rx - ((rx - lx1) / 2)

        self.canvas.coords('upper_handle', between_handles - 25, uy, between_handles + 25, uy1)
        self.canvas.coords('lower_handle', between_handles - 25, loy, between_handles + 25, loy1)



    def update_handles_pos_vert(self):
        _, uy, _, uy1 = self.canvas.coords('upper_handle')
        _, loy, _, loy1 = self.canvas.coords('lower_handle')

        lx, _, lx1, _ = self.canvas.coords('left_handle')
        rx, _, rx1, _ = self.canvas.coords('right_handle')

        between_handles = uy - ((uy - loy1) / 2)

        self.canvas.coords('left_handle', lx, between_handles - 25, lx1, between_handles + 25)
        self.canvas.coords('right_handle', rx, between_handles - 25, rx1, between_handles + 25)

    # def configure_widgets(self):
    #     self.canvas.bind("<Motion>", self.change_cursor)

    def in_crop_area_check(self, event):
        uy1 = self.canvas.coords('upper_handle')[3]
        loy = self.canvas.coords('lower_handle')[1]
        lx1 = self.canvas.coords('left_handle')[2]
        rx = self.canvas.coords('right_handle')[0]

        if event.x > lx1 and event.x < rx and event.y > uy1 and event.y < loy:
            return True

        return False

    def change_cursor(self, event):
        # cursors = ['fleur', 'sizing', 'sb_h_double_arrow', 'sb_v_double_arrow']
        if self.in_crop_area_check(event):
            self.canvas.config(cursor='fleur')
        else:
            self.canvas.config(cursor='arrow')
