class Cropping_area:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.create_handles()
        self.create_dashed_lines()

    def create_handles(self):
        width = self.width
        height = self.height

        left_coords = 0, height / 2 - 25, 5, height / 2 + 25
        right_coords = width, height / 2 - 25, width - 5, height / 2 + 25
        up_coords = width / 2 - 25, 0, width / 2 + 25, 5
        down_coords = width / 2 - 25, height, width / 2 + 25, height - 5

        upper_left_coords = 0, 0, 0, 50, 5, 50, 5, 5, 50, 5, 50, 0
        lower_left_coords = 0, height, 0, height-50, 5, height-50, 5, height-5,  50, height-5, 50, height

        upper_right_coords = width, 0, width, 50, width-5, 50, width-5, 5, width-50, 5, width-50, 0
        lower_right_coords = (
            width, height, width, height-50, width-5, height-50, width-5, height-5, width-50,
            height-5, width-50, height
        )
        self.canvas.create_rectangle(up_coords, fill='white', tag = 'upper_handle')
        self.canvas.create_rectangle(down_coords, fill='white', tag='lower_handle')
        self.canvas.create_rectangle(left_coords, fill='white', tag='left_handle')
        self.canvas.create_rectangle(right_coords, fill='white', tag='right_handle')

        self.canvas.create_polygon(upper_left_coords, fill='white', tag='upper_left_handle', outline='black')
        self.canvas.create_polygon(lower_left_coords, fill='white', tag='lower_left_handle', outline='black')
        self.canvas.create_polygon(upper_right_coords, fill='white', tag='upper_right_handle', outline='black')
        self.canvas.create_polygon(lower_right_coords, fill='white', tag='lower_right_handle', outline='black')

        self.canvas.tag_bind(
            'upper_left_handle', '<B1-Motion>', self.upper_left_handle_move
        )
        self.canvas.tag_bind(
            'upper_left_handle', "<ButtonPress-1>",
            lambda event, tag='upper_left_handle': self.angle_move_start(event, tag)
        )
        self.canvas.tag_bind(
            'lower_left_handle', '<B1-Motion>', self.lower_left_handle_move
        )
        self.canvas.tag_bind(
            'lower_left_handle', "<ButtonPress-1>",
            lambda event, tag='lower_left_handle': self.angle_move_start(event, tag)
        )
        self.canvas.tag_bind(
            'upper_right_handle', '<B1-Motion>', self.upper_right_handle_move
        )
        self.canvas.tag_bind(
            'upper_right_handle', "<ButtonPress-1>",
            lambda event, tag='upper_right_handle': self.angle_move_start(event, tag)
        )
        self.canvas.tag_bind(
            'lower_right_handle', '<B1-Motion>', self.lower_right_handle_move
        )
        self.canvas.tag_bind(
            'lower_right_handle', "<ButtonPress-1>",
            lambda event, tag='lower_right_handle': self.angle_move_start(event, tag)
        )


        self.canvas.tag_bind(
            'upper_handle', '<B1-Motion>', lambda event, tag='upper_handle': self.move_vert(event, tag)
        )
        self.canvas.tag_bind(
            'upper_handle', "<ButtonPress-1>", lambda event, tag='upper_handle': self.move_start_vert(event, tag)
        )
        self.canvas.tag_bind(
            'lower_handle', '<B1-Motion>', lambda event, tag='lower_handle': self.move_vert(event, tag)
        )
        self.canvas.tag_bind(
            'lower_handle', "<ButtonPress-1>", lambda event, tag='lower_handle': self.move_start_vert(event, tag)
        )
        self.canvas.tag_bind(
            'left_handle', '<B1-Motion>', lambda event, tag='left_handle': self.move_hor(event, tag)
        )
        self.canvas.tag_bind(
            'left_handle', "<ButtonPress-1>", lambda event, tag='left_handle': self.move_start_hor(event, tag)
        )
        self.canvas.tag_bind(
            'right_handle', '<B1-Motion>', lambda event, tag='right_handle': self.move_hor(event, tag)
        )
        self.canvas.tag_bind(
            'right_handle', "<ButtonPress-1>", lambda event, tag='right_handle': self.move_start_hor(event, tag)
        )

    def create_dashed_lines(self):
        self.canvas.create_line(50,3,658,3, dash=(10,), fill='white', width=2, tag='upper_left_line')
        self.canvas.create_line(708,3,1315,3, dash=(10,), fill='white', width=2, tag='upper_right_line')
        self.canvas.create_line(3,50,3,359, dash=(10,), fill='white', width=2, tag='left_upper_line')
        self.canvas.create_line(3,409,3,718, dash=(10,), fill='white', width=2, tag='left_lower_line')
        self.canvas.create_line(50,765,658,765, dash=(10,), fill='white', width=2, tag='lower_left_line')
        self.canvas.create_line(708,765,1315,765, dash=(10,), fill='white', width=2, tag='lower_right_line')
        self.canvas.create_line(1363,718,1363,409, dash=(10,), fill='white', width=2, tag='right_lower_line')
        self.canvas.create_line(1363,50,1363,359,dash=(10,), fill='white', width=2, tag='right_upper_line')

    def update_lines_pos_hor(self, tag):
        if tag == 'left_handle':
            x = self.canvas.coords(tag)[0]

            luy,luy1 = self.canvas.coords('left_upper_line')[1::2]
            lly,lly1 = self.canvas.coords('left_lower_line')[1::2]

            self.canvas.coords('left_upper_line', x+3, luy, x+3, luy1)
            self.canvas.coords('left_lower_line', x+3, lly, x+3, lly1)

        if tag == 'right_handle':
            x = self.canvas.coords(tag)[0]

            ruy,ruy1 = self.canvas.coords('right_upper_line')[1::2]
            rly,rly1 = self.canvas.coords('right_lower_line')[1::2]

            self.canvas.coords('right_upper_line', x+3, ruy, x+3, ruy1)
            self.canvas.coords('right_lower_line', x+3, rly, x+3, rly1)

    def update_lines_pos_vert(self, tag):
        if tag == 'upper_handle':
            y = self.canvas.coords(tag)[1]

            ulx, ulx1 = self.canvas.coords('upper_left_line')[::2]
            urx, urx1 = self.canvas.coords('upper_right_line')[::2]

            self.canvas.coords('upper_left_line', ulx, y+3, ulx1, y+3)
            self.canvas.coords('upper_right_line', urx, y+3, urx1, y+3)

            self.update_perpendicular_lines_vert()

        if tag == 'lower_handle':
            y = self.canvas.coords(tag)[1]

            llx, llx1 = self.canvas.coords('lower_left_line')[::2]
            lrx, lrx1 = self.canvas.coords('lower_right_line')[::2]

            self.canvas.coords('lower_left_line', llx, y+3, llx1, y+3)
            self.canvas.coords('lower_right_line', lrx, y+3, lrx1, y+3)

            self.update_perpendicular_lines_vert()

    def update_perpendicular_lines_vert(self):
        ury = self.canvas.coords('upper_right_handle')[3]
        ly = self.canvas.coords('left_handle')[1]

        lux, lux1 = self.canvas.coords('left_upper_line')[::2]
        self.canvas.coords('left_upper_line', lux, ury, lux1, ly)

        rux, rux1 = self.canvas.coords('right_upper_line')[::2]
        self.canvas.coords('right_upper_line', rux, ury, rux1, ly)

        lry = self.canvas.coords('lower_right_handle')[3]
        ly = self.canvas.coords('left_handle')[3]

        llx, llx1 = self.canvas.coords('left_lower_line')[::2]
        self.canvas.coords('left_lower_line', llx, lry, llx1, ly)

        rlx, rlx1 = self.canvas.coords('right_lower_line')[::2]
        self.canvas.coords('right_lower_line', rlx, lry, rlx1, ly)

    def get_tags_for_angle_movement(self, tag):
        if tag == 'upper_left_handle':
            return 'left_handle', 'upper_handle', 'lower_left_handle', 'upper_right_handle'
        elif tag == 'upper_right_handle':
            return 'right_handle', 'upper_handle', 'lower_right_handle', 'upper_left_handle'
        elif tag == 'lower_left_handle':
            return 'left_handle', 'lower_handle', 'upper_left_handle', 'lower_right_handle'
        else:
            return 'right_handle', 'lower_handle', 'lower_left_handle', 'upper_right_handle'

    def upper_left_handle_move(self, event):
        x, y = event.x + self.difference[0], event.y + self.difference[1]
        self.canvas.coords(
            'upper_left_handle', x, y, x, y + 50, x + 5, y + 50, x + 5, y + 5, x + 50, y + 5, x + 50, y
        )

        self.move_vert(event, 'upper_handle')
        self.move_hor(event, 'left_handle')

    def upper_right_handle_move(self, event):
        x, y = event.x + self.difference[0], event.y + self.difference[1]
        self.canvas.coords(
            'upper_right_handle', x, y, x, y + 50, x - 5, y + 50, x - 5, y + 5, x - 50, y + 5, x - 50, y
        )

        self.move_vert(event, 'upper_handle')
        self.move_hor(event, 'right_handle')

    def lower_left_handle_move(self, event):
        x, y = event.x + self.difference[0], event.y + self.difference[1]
        self.canvas.coords(
            'lower_left_handle', x, y, x, y - 50, x + 5, y - 50, x + 5, y - 5, x + 50, y - 5, x + 50, y
        )

        self.move_vert(event, 'lower_handle')
        self.move_hor(event, 'left_handle')

    def lower_right_handle_move(self, event):
        x, y = event.x + self.difference[0], event.y + self.difference[1]
        self.canvas.coords(
            'lower_right_handle', x, y, x, y - 50, x - 5, y - 50, x - 5, y - 5, x - 50, y - 5, x - 50, y
        )

        self.move_vert(event, 'lower_handle')
        self.move_hor(event, 'right_handle')

    def angle_move_start(self, event, tag):
        coords = self.canvas.coords(tag)[0:2]
        self.difference = coords[0] - event.x, coords[1] - event.y

    def move_start_hor(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.to_left_border = event.x - x
        self.to_right_border = x1 - event.x

    def move_hor(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.canvas.coords(tag, event.x-self.to_left_border, y, event.x+self.to_right_border, y1)

        self.angle_handles_update_hor(tag)
        self.update_handles_pos_hor()
        self.update_lines_pos_hor(tag)

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

        if handle_tag == 'left_handle':
            x = self.canvas.coords(handle_tag)[0]

            x0,y0, x1,y1, x2,y2, x3,y3, x4,y4, x5,y5 = self.canvas.coords(upper_handle)
            self.canvas.coords(upper_handle, x,y0, x,y1, x+5,y2, x+5,y3, x+50,y4, x+50,y5)

            x0,y0, x1,y1, x2,y2, x3,y3, x4,y4, x5,y5 = self.canvas.coords(lower_handle)
            self.canvas.coords(lower_handle, x,y0, x,y1, x+5,y2, x+5,y3, x+50,y4, x+50,y5)
        else:
            x = self.canvas.coords(handle_tag)[2]

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(upper_handle)
            self.canvas.coords(upper_handle, x, y0, x, y1, x-5, y2, x-5, y3, x-50, y4, x-50, y5)

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(lower_handle)
            self.canvas.coords(lower_handle, x, y0, x, y1, x-5, y2, x-5, y3, x-50, y4, x-50, y5)

    def angle_handles_update_vert(self, handle_tag):
        upper_handle, lower_handle = self.get_angle_handle_tags(handle_tag)

        if handle_tag == 'upper_handle':
            y = self.canvas.coords(handle_tag)[1]

            x0,y0, x1,y1, x2,y2, x3,y3, x4,y4, x5,y5 = self.canvas.coords(upper_handle)
            self.canvas.coords(upper_handle, x0,y, x1,y+50, x2,y+50, x3,y+5, x4,y+5, x5,y)

            x0,y0, x1,y1, x2,y2, x3,y3, x4,y4, x5,y5 = self.canvas.coords(lower_handle)
            self.canvas.coords(lower_handle, x0,y, x1,y+50, x2,y+50, x3,y+5, x4,y+5, x5,y)
        else:
            y = self.canvas.coords(handle_tag)[3]

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(upper_handle)
            self.canvas.coords(upper_handle, x0, y, x1, y-50, x2, y-50, x3, y-5, x4, y-5, x5, y)

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(lower_handle)
            self.canvas.coords(lower_handle, x0, y, x1, y-50, x2, y-50, x3, y-5, x4, y-5, x5, y)

    def move_vert(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.canvas.coords(tag, x, event.y-self.to_upper_border, x1, event.y+self.to_lower_border)

        self.angle_handles_update_vert(tag)
        self.update_handles_pos_vert()
        self.update_lines_pos_vert(tag)

    def update_handles_pos_hor(self):
        lx, _, lx1, _ = self.canvas.coords('left_handle')
        rx, _, rx1, _ = self.canvas.coords('right_handle')

        _, uy, _, uy1 = self.canvas.coords('upper_handle')
        _, loy, _, loy1 = self.canvas.coords('lower_handle')

        between_handles = rx - ((rx - lx1) / 2)

        self.canvas.coords('upper_handle', between_handles - 25, uy, between_handles + 25, uy1)
        self.canvas.coords('lower_handle', between_handles - 25, loy, between_handles + 25, loy1)

        self.update_lines_pos_hor('upper_handle')
        self.update_lines_pos_hor('lower_handle')

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
