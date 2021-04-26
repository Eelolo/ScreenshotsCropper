from PIL import ImageEnhance, ImageTk


class Cropping_area:
    def __init__(self, main):
        self.main = main
        self.canvas = self.main.img_canv
        self.width = self.main.width
        self.height = self.main.height
        self.create_handles()
        self.create_dashed_lines()
        self.configure_widgets()

        self.to_lower_border = 1
        self.to_upper_border = 4
        self.to_left_border = 1
        self.to_right_border = 4

        self.area_coords = 0, 0, self.width, 0, 0, self.height, self.width, self.height
        self.area = self.width, self.height

        self.btn_prssd = None

    def update_dark_mask(self, event=None):
        im = self.main.screenshot.copy()
        ulx, uly, _, _, _, _, lrx, lry = self.area_coords

        enhancer = ImageEnhance.Brightness(im)
        with_mask = enhancer.enhance(0.5)

        area = im.crop((int(ulx),int(uly),int(lrx),int(lry)))
        with_mask.paste(area, (int(ulx),int(uly),int(lrx),int(lry)))

        self.with_mask = ImageTk.PhotoImage(with_mask)
        self.canvas.itemconfigure('screenshot', image=self.with_mask)

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

        self.update_perpendicular_lines_hor()

    def update_lines_pos_vert(self, tag):
        if tag == 'upper_handle':
            y = self.canvas.coords(tag)[1]

            ulx, ulx1 = self.canvas.coords('upper_left_line')[::2]
            urx, urx1 = self.canvas.coords('upper_right_line')[::2]

            self.canvas.coords('upper_left_line', ulx, y+3, ulx1, y+3)
            self.canvas.coords('upper_right_line', urx, y+3, urx1, y+3)


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

    def update_perpendicular_lines_hor(self):
        ulx = self.canvas.coords('upper_left_handle')[8]
        ux = self.canvas.coords('upper_handle')[0]

        uly, uly1 = self.canvas.coords('upper_left_line')[1::2]
        self.canvas.coords('upper_left_line', ulx, uly, ux, uly1)

        lly, lly1 = self.canvas.coords('lower_left_line')[1::2]
        self.canvas.coords('lower_left_line', ulx, lly, ux, lly1)

        urx = self.canvas.coords('upper_right_handle')[8]
        ux = self.canvas.coords('upper_handle')[2]

        ury, ury1 = self.canvas.coords('upper_right_line')[1::2]
        self.canvas.coords('upper_right_line', ux, ury, urx, ury1)

        lry, lry1 = self.canvas.coords('lower_right_line')[1::2]
        self.canvas.coords('lower_right_line', ux, lry, urx, lry1)

    def update_area_coords(func):
        def wrapper(*args):
            func(*args)
            self = args[0]

            ulx, uly = self.canvas.coords('upper_left_handle')[:2]
            urx, ury = self.canvas.coords('upper_right_handle')[:2]
            llx, lly = self.canvas.coords('lower_left_handle')[:2]
            lrx, lry = self.canvas.coords('lower_right_handle')[:2]

            self.area_coords = ulx, uly, urx, ury, llx, lly, lrx, lry
            self.area = urx - ulx, lly - uly

        return wrapper

    @update_area_coords
    def upper_left_handle_move(self, event):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 =  self.canvas.coords('upper_left_handle')

        diff_x = event.x - self.angle_move_start_coords.x
        diff_y = event.y - self.angle_move_start_coords.y

        if x0 + diff_x >= 0 and y0 + diff_y >=0:
            self.canvas.coords(
                'upper_left_handle',
                x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y,
                x2 + diff_x, y2 + diff_y, x3 + diff_x, y3 + diff_y,
                x4 + diff_x, y4 + diff_y, x5 + diff_x, y5 + diff_y
            )
            self.angle_move_start_coords = event

            self.move_vert(event, 'upper_handle')
            self.move_hor(event, 'left_handle')

    @update_area_coords
    def upper_right_handle_move(self, event):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('upper_right_handle')

        diff_x = event.x - self.angle_move_start_coords.x
        diff_y = event.y - self.angle_move_start_coords.y

        if x0 + diff_x <= self.width and y0 + diff_y >= 0:
            self.canvas.coords(
                'upper_right_handle',
                x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y,
                x2 + diff_x, y2 + diff_y, x3 + diff_x, y3 + diff_y,
                x4 + diff_x, y4 + diff_y, x5 + diff_x, y5 + diff_y
            )
            self.angle_move_start_coords = event

            self.move_vert(event, 'upper_handle')
            self.move_hor(event, 'right_handle')

    @update_area_coords
    def lower_left_handle_move(self, event):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('lower_left_handle')

        diff_x = event.x - self.angle_move_start_coords.x
        diff_y = event.y - self.angle_move_start_coords.y

        if x0 + diff_x >= 0 and y0 + diff_y <= self.height:
            self.canvas.coords(
                'lower_left_handle',
                x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y,
                x2 + diff_x, y2 + diff_y, x3 + diff_x, y3 + diff_y,
                x4 + diff_x, y4 + diff_y, x5 + diff_x, y5 + diff_y
            )
            self.angle_move_start_coords = event

            self.move_vert(event, 'lower_handle')
            self.move_hor(event, 'left_handle')

    @update_area_coords
    def lower_right_handle_move(self, event):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('lower_right_handle')

        diff_x = event.x - self.angle_move_start_coords.x
        diff_y = event.y - self.angle_move_start_coords.y

        if x0 + diff_x <= self.width and y0 + diff_y <= self.height:
            self.canvas.coords(
                'lower_right_handle',
                x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y,
                x2 + diff_x, y2 + diff_y, x3 + diff_x, y3 + diff_y,
                x4 + diff_x, y4 + diff_y, x5 + diff_x, y5 + diff_y
            )
            self.angle_move_start_coords = event

            self.move_vert(event, 'lower_handle')
            self.move_hor(event, 'right_handle')

    def angle_move_start(self, event, tag):
        coords = self.canvas.coords(tag)[0:2]
        self.difference = coords[0] - event.x, coords[1] - event.y
        self.angle_move_start_coords = event

        self.btn_prssd = tag

    def move_start_hor(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.to_left_border = event.x - x
        self.to_right_border = x1 - event.x

        self.btn_prssd = tag

    @update_area_coords
    def move_hor(self, event, tag):
        if event.x - self.to_left_border >= 0 and event.x + self.to_right_border <= self.width:
            y, y1 = self.canvas.coords(tag)[1::2]
            self.canvas.coords(tag, event.x - self.to_left_border, y, event.x + self.to_right_border, y1)

            self.angle_handles_update_hor(tag)
            self.update_handles_pos_hor()
            self.update_lines_pos_hor(tag)
            self.update_dark_mask()

    def move_start_vert(self, event, tag):
        x, y, x1, y1 = self.canvas.coords(tag)
        self.to_upper_border = event.y - y
        self.to_lower_border = y1 - event.y
        self.event = event

        self.btn_prssd = tag

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

    @update_area_coords
    def move_vert(self, event, tag):
        if event.y - self.to_upper_border >= 0 and event.y + self.to_lower_border <= self.height:
            x, x1 = self.canvas.coords(tag)[::2]
            self.canvas.coords(tag, x, event.y - self.to_upper_border, x1, event.y + self.to_lower_border)

            self.angle_handles_update_vert(tag)
            self.update_handles_pos_vert()
            self.update_lines_pos_vert(tag)
            self.update_dark_mask()

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

    def configure_widgets(self):
        self.canvas.bind("<Motion>", self.change_cursor)
        self.canvas.bind('<ButtonPress-1>', self.define_move_start_function)
        self.canvas.bind('<B1-Motion>', self.define_move_function)
        self.canvas.bind('<ButtonRelease-1>', self.button_release)

    def button_release(self, event):
        self.btn_prssd = None
        self.update_dark_mask()

    def define_move_start_function(self, event):
        if not self.btn_prssd:
            if self.in_crop_area_check(event):
                self.area_move_start(event)
            elif self.in_gor_move_area_check(event):
                if event.x < self.area_coords[0] + self.area[0] / 2:
                    self.move_start_hor(event, 'left_handle')
                else:
                    self.move_start_hor(event, 'right_handle')
            elif self.in_vert_move_area_check(event):
                if event.y > self.area_coords[1] + self.area[1] / 2:
                    self.move_start_vert(event, 'lower_handle')
                else:
                    self.move_start_vert(event, 'upper_handle')

            elif self.in_angles_move_area_check(event):
                if event.x < self.area_coords[0] + self.area[0] / 2:
                    if event.y > self.area_coords[1] + self.area[1] / 2:
                        self.angle_move_start(event, 'lower_left_handle')
                    else:
                        self.angle_move_start(event, 'upper_left_handle')
                else:
                    if event.y > self.area_coords[1] + self.area[1] / 2:
                        self.angle_move_start(event, 'lower_right_handle')
                    else:
                        self.angle_move_start(event, 'upper_right_handle')

    def define_move_function(self, event):
        if self.btn_prssd == 'area':
            self.area_move(event)
        elif self.btn_prssd == 'left_handle':
            self.move_hor(event, 'left_handle')
        elif self.btn_prssd == 'right_handle':
            self.move_hor(event, 'right_handle')
        elif self.btn_prssd == 'lower_handle':
            self.move_vert(event, 'lower_handle')
        elif self.btn_prssd == 'upper_handle':
            self.move_vert(event, 'upper_handle')
        elif self.btn_prssd == 'lower_left_handle':
            self.lower_left_handle_move(event)
        elif self.btn_prssd == 'upper_left_handle':
            self.upper_left_handle_move(event)
        elif self.btn_prssd == 'lower_right_handle':
            self.lower_right_handle_move(event)
        else:
            self.upper_right_handle_move(event)

    def in_crop_area_check(self, event):
        uy1 = self.canvas.coords('upper_handle')[3]
        loy = self.canvas.coords('lower_handle')[1]
        lx1 = self.canvas.coords('left_handle')[2]
        rx = self.canvas.coords('right_handle')[0]

        indent_x = int(self.area[0] / 6)
        indent_y = int(self.area[1] / 6)

        if lx1 + indent_x < event.x < rx - indent_x and event.y > uy1 + indent_y and event.y < loy - indent_y:
            return True

        return False

    def in_gor_move_area_check(self, event):
        lx, ly, lx1, ly1 = self.canvas.coords('left_handle')
        rx, ry, rx1, ry1 = self.canvas.coords('right_handle')

        indent_x = int(self.area[0] / 6)
        indent_y = int(self.area[1] / 6)

        if lx - indent_x < event.x < lx1 + indent_x and ly - indent_y < event.y < ly1 + indent_y:
            return True
        elif rx - indent_x < event.x < rx1 + indent_x and ry - indent_y < event.y < ry1 + indent_y:
            return True

        return False

    def in_vert_move_area_check(self, event):
        ux, uy, ux1, uy1 = self.canvas.coords('upper_handle')
        lx, ly, lx1, ly1 = self.canvas.coords('lower_handle')

        indent_x = int(self.area[0] / 6)
        indent_y = int(self.area[1] / 6)

        if lx - indent_x < event.x < lx1 + indent_x and ly - indent_y < event.y < ly1 + indent_y:
            return True
        elif ux - indent_x < event.x < ux1 + indent_x and uy - indent_y < event.y < uy1 + indent_y:
            return True

        return False

    def in_angles_move_area_check(self, event):
        x, y = self.area_coords[:2]
        y1, x1 = self.area_coords[:-3:-1]

        indent_x = int(self.area[0] / 6)
        indent_y = int(self.area[1] / 6)

        if x - indent_x < event.x < x1 + indent_x and y - indent_y < event.y < y1 + indent_y:
            return True

        return False

    def change_cursor(self, event):
        if self.in_crop_area_check(event):
            self.canvas.config(cursor='fleur')
        elif self.in_gor_move_area_check(event):
            self.canvas.config(cursor='sb_h_double_arrow')
        elif self.in_vert_move_area_check(event):
            self.canvas.config(cursor='sb_v_double_arrow')
        elif self.in_angles_move_area_check(event):
            if event.x < self.area_coords[0] + self.area[0] / 2:
                if event.y > self.area_coords[1] + self.area[1] / 2:
                    self.canvas.config(cursor='top_right_corner')
                else:
                    self.canvas.config(cursor='bottom_right_corner')
            else:
                if event.y > self.area_coords[1] + self.area[1] / 2:
                    self.canvas.config(cursor='top_left_corner')
                else:
                    self.canvas.config(cursor='bottom_left_corner')
        else:
            self.canvas.config(cursor='arrow')

    def area_move_start(self, event):
        self.btn_prssd = 'area'
        self.area_move_start_coords = event

    @update_area_coords
    def area_move(self, event):
        diff_x = event.x - self.area_move_start_coords.x
        diff_y = event.y - self.area_move_start_coords.y

        x0, y0, x1, y1 = self.canvas.coords('upper_handle')
        self.canvas.coords('upper_handle', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('lower_handle')
        self.canvas.coords('lower_handle', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('left_handle')
        self.canvas.coords('left_handle', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('right_handle')
        self.canvas.coords('right_handle', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)

        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('upper_left_handle')
        self.canvas.coords(
            'upper_left_handle',
            x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y,
            x2 + diff_x, y2 + diff_y, x3 + diff_x, y3 + diff_y,
            x4 + diff_x, y4 + diff_y, x5 + diff_x, y5 + diff_y
        )
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('lower_left_handle')
        self.canvas.coords(
            'lower_left_handle',
            x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y,
            x2 + diff_x, y2 + diff_y, x3 + diff_x, y3 + diff_y,
            x4 + diff_x, y4 + diff_y, x5 + diff_x, y5 + diff_y
        )
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('upper_right_handle')
        self.canvas.coords(
            'upper_right_handle',
            x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y,
            x2 + diff_x, y2 + diff_y, x3 + diff_x, y3 + diff_y,
            x4 + diff_x, y4 + diff_y, x5 + diff_x, y5 + diff_y
        )
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('lower_right_handle')
        self.canvas.coords(
            'lower_right_handle',
            x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y,
            x2 + diff_x, y2 + diff_y, x3 + diff_x, y3 + diff_y,
            x4 + diff_x, y4 + diff_y, x5 + diff_x, y5 + diff_y
        )

        x0, y0, x1, y1 = self.canvas.coords('upper_left_line')
        self.canvas.coords('upper_left_line', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('upper_right_line')
        self.canvas.coords('upper_right_line', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('left_upper_line')
        self.canvas.coords('left_upper_line', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('left_lower_line')
        self.canvas.coords('left_lower_line', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('lower_left_line')
        self.canvas.coords('lower_left_line', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('lower_right_line')
        self.canvas.coords('lower_right_line', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('right_lower_line')
        self.canvas.coords('right_lower_line', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)
        x0, y0, x1, y1 = self.canvas.coords('right_upper_line')
        self.canvas.coords('right_upper_line', x0 + diff_x, y0 + diff_y, x1 + diff_x, y1 + diff_y)

        self.area_move_start_coords = event

        self.update_dark_mask()
