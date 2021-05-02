from PIL import ImageEnhance, ImageTk
from confirm_btns import ButtonsMenu


class CroppingArea:
    def __init__(self, main):
        self.main = main
        self.canvas = self.main.img_canv
        self.width = self.main.width
        self.height = self.main.height

        self.handle_width = 5
        self.handle_height = 50
        self.line_width = int(self.handle_width / 2)

        self.area_coords = 0, 0, self.width, 0, 0, self.height, self.width, self.height
        self.area = self.width, self.height

        self.btn_pressed = None

        self.create_handles()
        self.create_dashed_lines()
        self.configure_widgets()
        self.create_buttons()

    def create_buttons(self):
        self.btns_menu = ButtonsMenu(self.main, self)

    def create_handles(self):
        img_w = self.width
        img_h = self.height
        center_x = img_w / 2
        center_y = img_h / 2
        h_h = self.handle_height
        h_w = self.handle_width

        left_coords = 0, center_y - h_h / 2, h_w, center_y + h_h / 2
        right_coords = img_w, center_y - h_h / 2, img_w - h_w, center_y + h_h / 2
        up_coords = center_x - h_h / 2, 0, center_x + h_h / 2, h_w
        down_coords = center_x - h_h / 2, img_h, center_x + h_h / 2, img_h - h_w

        upper_left_coords = 0, 0, 0, h_h, h_w, h_h, h_w, h_w, h_h, h_w, h_h, 0

        lower_left_coords = (
            0, img_h, 0, img_h - h_h, h_w, img_h - h_h, h_w, img_h - h_w, h_h, img_h - h_w, h_h, img_h
        )
        upper_right_coords = (
            img_w, 0, img_w, h_h, img_w - h_w, h_h, img_w - h_w, h_w, img_w - h_h, h_w, img_w - h_h, 0
        )
        lower_right_coords = (
            img_w, img_h, img_w, img_h - h_h, img_w - h_w, img_h - h_h, img_w - h_w, img_h - h_w, img_w - h_h,
            img_h - h_w, img_w - h_h, img_h
        )
        self.canvas.create_rectangle(up_coords, fill='white', tag='upper_handle')
        self.canvas.create_rectangle(down_coords, fill='white', tag='lower_handle')
        self.canvas.create_rectangle(left_coords, fill='white', tag='left_handle')
        self.canvas.create_rectangle(right_coords, fill='white', tag='right_handle')

        self.canvas.create_polygon(upper_left_coords, fill='white', tag='upper_left_handle', outline='black')
        self.canvas.create_polygon(lower_left_coords, fill='white', tag='lower_left_handle', outline='black')
        self.canvas.create_polygon(upper_right_coords, fill='white', tag='upper_right_handle', outline='black')
        self.canvas.create_polygon(lower_right_coords, fill='white', tag='lower_right_handle', outline='black')

    def create_dashed_lines(self):
        img_w = self.width
        img_h = self.height
        center_x = img_w / 2
        center_y = img_h / 2
        h_h = self.handle_height
        h_w = self.handle_width
        pad_lor = int(h_w / 2)
        pad_lu = h_w - pad_lor
        l_w = self.line_width

        upper_left_line = h_h, pad_lu, center_x - h_h / 2, pad_lu
        upper_right_line = center_x + h_h / 2, pad_lu, img_w - h_h, pad_lu
        left_upper_line = pad_lu, h_h, pad_lu, center_y - h_h / 2
        left_lower_line = pad_lu, center_y + h_h / 2, pad_lu, img_h - h_h
        lower_left_line = h_h, img_h - pad_lor, center_x - h_h / 2, img_h - pad_lor
        lower_right_line = center_x + h_h / 2, img_h - pad_lor, img_w - h_h, img_h - pad_lor
        right_lower_line = img_w - pad_lor, img_h - h_h, img_w - pad_lor, center_y + h_h / 2
        right_upper_line = img_w - pad_lor, h_h, img_w - pad_lor, center_y - h_h / 2

        self.canvas.create_line(upper_left_line, dash=(10,), fill='white', width=l_w, tag='upper_left_line')
        self.canvas.create_line(upper_right_line, dash=(10,), fill='white', width=l_w, tag='upper_right_line')
        self.canvas.create_line(left_upper_line, dash=(10,), fill='white', width=l_w, tag='left_upper_line')
        self.canvas.create_line(left_lower_line, dash=(10,), fill='white', width=l_w, tag='left_lower_line')
        self.canvas.create_line(lower_left_line, dash=(10,), fill='white', width=l_w, tag='lower_left_line')
        self.canvas.create_line(lower_right_line, dash=(10,), fill='white', width=l_w, tag='lower_right_line')
        self.canvas.create_line(right_lower_line, dash=(10,), fill='white', width=l_w, tag='right_lower_line')
        self.canvas.create_line(right_upper_line, dash=(10,), fill='white', width=l_w, tag='right_upper_line')

    def update_lines_pos_hor(self, tag):
        if tag == 'left_handle':
            tag0 = 'left_upper_line'
            tag1 = 'left_lower_line'
        elif tag == 'right_handle':
            tag0 = 'right_upper_line'
            tag1 = 'right_lower_line'

        if tag in ('left_handle', 'right_handle'):
            x = self.canvas.coords(tag)[0]
            pad = self.handle_width / 2

            y0, y1 = self.canvas.coords(tag0)[1::2]
            y2, y3 = self.canvas.coords(tag1)[1::2]

            self.canvas.coords(tag0, x + pad, y0, x + pad, y1)
            self.canvas.coords(tag1, x + pad, y2, x + pad, y3)

        self.update_perpendicular_lines_hor()

    def update_lines_pos_vert(self, tag):
        if tag == 'upper_handle':
            tag0 = 'upper_left_line'
            tag1 = 'upper_right_line'
        elif tag == 'lower_handle':
            tag0 = 'lower_left_line'
            tag1 = 'lower_right_line'

        if tag in ('upper_handle', 'lower_handle'):
            y = self.canvas.coords(tag)[1]
            pad = self.handle_width / 2

            x0, x1 = self.canvas.coords(tag0)[::2]
            x2, x3 = self.canvas.coords(tag1)[::2]

            self.canvas.coords(tag0, x0, y + pad, x1, y + pad)
            self.canvas.coords(tag1, x2, y + pad, x3, y + pad)

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

    def update_dark_mask(func):
        def wrapper(*args):
            func(*args)
            self = args[0]

            image = self.main.screenshot.copy()
            ulx, uly, _, _, _, _, lrx, lry = self.area_coords

            enhancer = ImageEnhance.Brightness(image)
            with_mask = enhancer.enhance(0.5)

            area = image.crop((int(ulx), int(uly), int(lrx), int(lry)))
            with_mask.paste(area, (int(ulx), int(uly), int(lrx), int(lry)))

            self.with_mask = ImageTk.PhotoImage(with_mask)
            self.canvas.itemconfigure('screenshot', image=self.with_mask)

        return wrapper

    def angle_move_start(self, event, tag):
        self.angle_move_start_coords = event

        x0, y0, x1, y1, x2, y2, x3, y3 = self.area_coords
        self.start_edge_dist_l = x0 - event.x
        self.start_edge_dist_r = x1 - event.x
        self.start_edge_dist_u = y0 - event.y
        self.start_edge_dist_d = y2 - event.y

        self.btn_pressed = tag

    def add_difference(self, array, diff_x=0, diff_y=0):
        start = 0
        step = 1

        if diff_x and not diff_y:
            step = 2
        elif diff_y and not diff_x:
            start = 1
            step = 2

        for idx in range(start, len(array), step):
            if idx == 0 or idx % 2 == 0:
                array[idx] += diff_x

            if idx != 0 and idx % 2 != 0:
                array[idx] += diff_y

        return array

    @update_area_coords
    @update_dark_mask
    def upper_left_handle_move(self, event):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('upper_left_handle')

        diff_x = event.x - self.angle_move_start_coords.x
        diff_y = event.y - self.angle_move_start_coords.y

        edge_dist_l = x0 - event.x
        edge_dist_u = y0 - event.y

        if x0 + diff_x < 0 or x0 == 0 and edge_dist_l > self.start_edge_dist_l:
            diff_x = 0 - x0

        if y0 + diff_y < 0 or y0 == 0 and edge_dist_u > self.start_edge_dist_u:
            diff_y = 0 - y0

        ux = int(self.canvas.coords('upper_handle')[0])
        if x4 + diff_x >  ux or int(x4) == ux and edge_dist_l < self.start_edge_dist_l:
            diff_x = self.canvas.coords('upper_handle')[0] - x4

        ly = int(self.canvas.coords('left_handle')[1])
        if y1 + diff_y >  ly or int(y1) == ly and edge_dist_u < self.start_edge_dist_u:
            diff_y = self.canvas.coords('left_handle')[1] - y1

        points = self.add_difference(self.canvas.coords('upper_left_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_left_handle', points)

        points = self.add_difference(self.canvas.coords('left_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('left_handle', points)

        points = self.add_difference(self.canvas.coords('upper_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_handle', points)

        points = self.add_difference(self.canvas.coords('lower_left_handle'), diff_x=diff_x)
        self.canvas.coords('lower_left_handle', points)

        points = self.add_difference(self.canvas.coords('upper_right_handle'), diff_y=diff_y)
        self.canvas.coords('upper_right_handle', points)

        self.angle_move_start_coords = event

        self.update_handles_pos_vert()
        self.update_handles_pos_hor()
        self.update_lines_pos_hor('left_handle')
        self.update_lines_pos_vert('upper_handle')

    @update_area_coords
    @update_dark_mask
    def upper_right_handle_move(self, event):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('upper_right_handle')

        diff_x = event.x - self.angle_move_start_coords.x
        diff_y = event.y - self.angle_move_start_coords.y

        edge_dist_r = x0 - event.x
        edge_dist_u = y0 - event.y

        if x0 + diff_x > self.width or x0 == self.width and edge_dist_r < self.start_edge_dist_r:
            diff_x = self.width - x0

        if y0 + diff_y < 0 or y0 == 0 and edge_dist_u > self.start_edge_dist_u:
            diff_y = 0 - y0

        ux = int(self.canvas.coords('upper_handle')[2])
        if x4 + diff_x < ux or int(x4) == ux and edge_dist_r > self.start_edge_dist_r:
            diff_x = self.canvas.coords('upper_handle')[2] - x4

        ry = int(self.canvas.coords('right_handle')[1])
        if y1 + diff_y > ry or int(y1) == ry and edge_dist_u < self.start_edge_dist_u:
            diff_y = self.canvas.coords('right_handle')[1] - y1

        points = self.add_difference(self.canvas.coords('upper_right_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_right_handle', points)

        points = self.add_difference(self.canvas.coords('right_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('right_handle', points)

        points = self.add_difference(self.canvas.coords('upper_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_handle', points)

        points = self.add_difference(self.canvas.coords('lower_right_handle'), diff_x=diff_x)
        self.canvas.coords('lower_right_handle', points)

        points = self.add_difference(self.canvas.coords('upper_left_handle'), diff_y=diff_y)
        self.canvas.coords('upper_left_handle', points)

        self.angle_move_start_coords = event

        self.update_handles_pos_vert()
        self.update_handles_pos_hor()
        self.update_lines_pos_hor('right_handle')
        self.update_lines_pos_vert('upper_handle')

    @update_area_coords
    @update_dark_mask
    def lower_left_handle_move(self, event):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('lower_left_handle')

        diff_x = event.x - self.angle_move_start_coords.x
        diff_y = event.y - self.angle_move_start_coords.y

        edge_dist_l = x0 - event.x
        edge_dist_d = y0 - event.y

        if x0 + diff_x < 0 or x0 == 0 and edge_dist_l > self.start_edge_dist_l:
            diff_x = 0 - x0

        if y0 + diff_y > self.height or y0 == self.height and edge_dist_d < self.start_edge_dist_d:
            diff_y = self.height - y0

        lx = int(self.canvas.coords('lower_handle')[0])
        if x4 + diff_x > lx or int(x4) == lx and edge_dist_l < self.start_edge_dist_l:
            diff_x = self.canvas.coords('lower_handle')[0] - x4

        ly = int(self.canvas.coords('left_handle')[3])
        if y2 + diff_y < ly or int(y2) == ly and edge_dist_d > self.start_edge_dist_d:
            diff_y = self.canvas.coords('left_handle')[3] - y2

        points = self.add_difference(self.canvas.coords('lower_left_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_left_handle', points)

        points = self.add_difference(self.canvas.coords('left_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('left_handle', points)

        points = self.add_difference(self.canvas.coords('lower_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_handle', points)

        points = self.add_difference(self.canvas.coords('upper_left_handle'), diff_x=diff_x)
        self.canvas.coords('upper_left_handle', points)

        points = self.add_difference(self.canvas.coords('lower_right_handle'), diff_y=diff_y)
        self.canvas.coords('lower_right_handle', points)

        self.angle_move_start_coords = event

        self.update_handles_pos_vert()
        self.update_handles_pos_hor()
        self.update_lines_pos_hor('left_handle')
        self.update_lines_pos_vert('lower_handle')

    @update_area_coords
    @update_dark_mask
    def lower_right_handle_move(self, event):
        x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords('lower_right_handle')

        diff_x = event.x - self.angle_move_start_coords.x
        diff_y = event.y - self.angle_move_start_coords.y

        edge_dist_r = x0 - event.x
        edge_dist_d = y0 - event.y

        if x0 + diff_x > self.width or x0 == self.width and edge_dist_r < self.start_edge_dist_r:
            diff_x = self.width - x0

        if y0 + diff_y > self.height or y0 == self.height and edge_dist_d < self.start_edge_dist_d:
            diff_y = self.height - y0

        lx = int(self.canvas.coords('lower_handle')[2])
        if x4 + diff_x < lx or int(x4) == lx and edge_dist_r > self.start_edge_dist_r:
            diff_x = self.canvas.coords('lower_handle')[2] - x4

        ry = int(self.canvas.coords('right_handle')[3])
        if y1 + diff_y < ry or int(y1) == ry and edge_dist_d > self.start_edge_dist_d:
            diff_y = self.canvas.coords('right_handle')[3] - y1

        points = self.add_difference(self.canvas.coords('lower_right_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_right_handle', points)

        points = self.add_difference(self.canvas.coords('right_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('right_handle', points)

        points = self.add_difference(self.canvas.coords('lower_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_handle', points)

        points = self.add_difference(self.canvas.coords('upper_right_handle'), diff_x=diff_x)
        self.canvas.coords('upper_right_handle', points )

        points = self.add_difference(self.canvas.coords('lower_left_handle'), diff_y=diff_y)
        self.canvas.coords('lower_left_handle', points)

        self.angle_move_start_coords = event

        self.update_handles_pos_vert()
        self.update_handles_pos_hor()
        self.update_lines_pos_hor('right_handle')
        self.update_lines_pos_vert('lower_handle')

    def move_start_hor(self, event, tag):
        self.move_start_hor_coords = event

        x0, x1 = self.canvas.coords(tag)[::2]
        self.start_edge_dist_l = x0 - event.x
        self.start_edge_dist_r = x1 - event.x

        self.btn_pressed = tag

    @update_area_coords
    @update_dark_mask
    def move_hor(self, event, tag):
        diff_x = event.x - self.move_start_hor_coords.x
        x0, y0, x1, y1 = self.canvas.coords(tag)

        edge_dist_l = x0 - event.x
        edge_dist_r = x1 - event.x

        if tag == 'left_handle':
            if x0 + diff_x < 0 or x0 == 0 and edge_dist_l > self.start_edge_dist_l:
                diff_x = 0 - x0

            rx = self.canvas.coords('right_handle')[0]
            if x0 + diff_x + 150 > rx or x0 + 145 == rx and edge_dist_l < self.start_edge_dist_l:
                diff_x = self.canvas.coords('right_handle')[2] - x0 - 150
        else:
            if x1 + diff_x > self.width or x1 == self.width and edge_dist_r < self.start_edge_dist_r:
                diff_x = self.width - x1

            lx = self.canvas.coords('left_handle')[0]
            if x1 + diff_x - 150 < lx or x1 - 150 == lx and edge_dist_r > self.start_edge_dist_r:
                diff_x = self.canvas.coords('left_handle')[0] - x1 + 150

        points = self.add_difference([x0, y0, x1, y1], diff_x=diff_x)
        self.canvas.coords(tag, points)

        self.angle_handles_update_hor(tag)
        self.update_handles_pos_vert()
        self.update_lines_pos_hor(tag)

        self.move_start_hor_coords = event

    def move_start_vert(self, event, tag):
        self.move_start_vert_coords = event

        y0, y1 = self.canvas.coords(tag)[1::2]
        self.start_edge_dist_u = y0 - event.y
        self.start_edge_dist_d = y1 - event.y

        self.btn_pressed = tag

    @update_area_coords
    @update_dark_mask
    def move_vert(self, event, tag):
        diff_y = event.y - self.move_start_vert_coords.y
        x0, y0, x1, y1 = self.canvas.coords(tag)

        edge_dist_u = y0 - event.y
        edge_dist_d = y1 - event.y

        if tag == 'upper_handle':
            if y0 + diff_y < 0 or y0 == 0 and edge_dist_u > self.start_edge_dist_u:
                diff_y = 0 - y0

            ly = self.canvas.coords('lower_handle')[1]
            if y0 + diff_y + 150 > ly or y0 + 145 == ly and edge_dist_u < self.start_edge_dist_u:
                diff_y = self.canvas.coords('lower_handle')[3] - y0 - 150
        else:
            if y1 + diff_y > self.height or y1 == self.height and edge_dist_d < self.start_edge_dist_d:
                diff_y = self.height - y1

            uy = self.canvas.coords('upper_handle')[1]
            if y1 + diff_y - 150 < uy or y1 - 150 == uy and edge_dist_d > self.start_edge_dist_d:
                diff_y = self.canvas.coords('upper_handle')[1] - y1 + 150

        points = self.add_difference([x0, y0, x1, y1], diff_y=diff_y)
        self.canvas.coords(tag, points)

        self.angle_handles_update_vert(tag)
        self.update_handles_pos_hor()
        self.update_lines_pos_vert(tag)

        self.move_start_vert_coords = event

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

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(upper_handle)
            self.canvas.coords(upper_handle, x, y0, x, y1, x + 5, y2, x + 5, y3, x + 50, y4, x + 50, y5)

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(lower_handle)
            self.canvas.coords(lower_handle, x, y0, x, y1, x + 5, y2, x + 5, y3, x + 50, y4, x + 50, y5)
        else:
            x = self.canvas.coords(handle_tag)[2]

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(upper_handle)
            self.canvas.coords(upper_handle, x, y0, x, y1, x - 5, y2, x - 5, y3, x - 50, y4, x - 50, y5)

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(lower_handle)
            self.canvas.coords(lower_handle, x, y0, x, y1, x - 5, y2, x - 5, y3, x - 50, y4, x - 50, y5)

    def angle_handles_update_vert(self, handle_tag):
        upper_handle, lower_handle = self.get_angle_handle_tags(handle_tag)

        if handle_tag == 'upper_handle':
            y = self.canvas.coords(handle_tag)[1]

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(upper_handle)
            self.canvas.coords(upper_handle, x0, y, x1, y + 50, x2, y + 50, x3, y + 5, x4, y + 5, x5, y)

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(lower_handle)
            self.canvas.coords(lower_handle, x0, y, x1, y + 50, x2, y + 50, x3, y + 5, x4, y + 5, x5, y)
        else:
            y = self.canvas.coords(handle_tag)[3]

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(upper_handle)
            self.canvas.coords(upper_handle, x0, y, x1, y - 50, x2, y - 50, x3, y - 5, x4, y - 5, x5, y)

            x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = self.canvas.coords(lower_handle)
            self.canvas.coords(lower_handle, x0, y, x1, y - 50, x2, y - 50, x3, y - 5, x4, y - 5, x5, y)

    def update_handles_pos_vert(self):
        lx, _, lx1, _ = self.canvas.coords('left_handle')
        rx, _, rx1, _ = self.canvas.coords('right_handle')

        _, uy, _, uy1 = self.canvas.coords('upper_handle')
        _, loy, _, loy1 = self.canvas.coords('lower_handle')

        between_handles = rx - ((rx - lx1) / 2)

        self.canvas.coords('upper_handle', between_handles - 25, uy, between_handles + 25, uy1)
        self.canvas.coords('lower_handle', between_handles - 25, loy, between_handles + 25, loy1)

        self.update_lines_pos_hor('upper_handle')
        self.update_lines_pos_hor('lower_handle')

    def update_handles_pos_hor(self):
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

    @update_dark_mask
    def button_release(self, event):
        self.btn_pressed = None

    def define_move_start_function(self, event):
        if not self.btn_pressed:
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
        if self.btn_pressed == 'area':
            self.area_move(event)
        elif self.btn_pressed == 'left_handle':
            self.move_hor(event, 'left_handle')
        elif self.btn_pressed == 'right_handle':
            self.move_hor(event, 'right_handle')
        elif self.btn_pressed == 'lower_handle':
            self.move_vert(event, 'lower_handle')
        elif self.btn_pressed == 'upper_handle':
            self.move_vert(event, 'upper_handle')
        elif self.btn_pressed == 'lower_left_handle':
            self.lower_left_handle_move(event)
        elif self.btn_pressed == 'upper_left_handle':
            self.upper_left_handle_move(event)
        elif self.btn_pressed == 'lower_right_handle':
            self.lower_right_handle_move(event)
        elif self.btn_pressed == 'upper_right_handle':
            self.upper_right_handle_move(event)

    def in_crop_area_check(self, event):
        uy1 = self.canvas.coords('upper_handle')[3]
        loy = self.canvas.coords('lower_handle')[1]
        lx1 = self.canvas.coords('left_handle')[2]
        rx = self.canvas.coords('right_handle')[0]

        indent_x = int(self.area[0] / 6)
        indent_y = int(self.area[1] / 6)

        if lx1 + indent_x < event.x < rx - indent_x and uy1 + indent_y < event.y < loy - indent_y:
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
        self.btn_pressed = 'area'
        self.area_move_start_coords = event

        x0, y0, x1, y1, x2, y2, x3, y3 = self.area_coords
        self.start_edge_dist_l = x0 - event.x
        self.start_edge_dist_r = x1 - event.x
        self.start_edge_dist_u = y0 - event.y
        self.start_edge_dist_d = y2 - event.y

    @update_area_coords
    @update_dark_mask
    def area_move(self, event):
        diff_x = event.x - self.area_move_start_coords.x
        diff_y = event.y - self.area_move_start_coords.y

        x0, y0, x1, y1, x2, y2, x3, y3 = self.area_coords
        edge_dist_l = x0 - event.x
        edge_dist_r = x1 - event.x
        edge_dist_u = y0 - event.y
        edge_dist_d = y2 - event.y

        if x0 + diff_x < 0 or x0 == 0 and edge_dist_l > self.start_edge_dist_l:
            diff_x = 0 - x0

        if x1 + diff_x > self.width or x1 == self.width and edge_dist_r < self.start_edge_dist_r:
            diff_x = self.width - x1

        if y0 + diff_y < 0 or y0 == 0 and edge_dist_u > self.start_edge_dist_u:
            diff_y = 0 - y0

        if y2 + diff_y > self.height or y2 == self.height and edge_dist_d < self.start_edge_dist_d:
            diff_y = self.height - y2

        points = self.add_difference(self.canvas.coords('upper_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_handle', points)
        points = self.add_difference(self.canvas.coords('lower_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_handle', points)
        points = self.add_difference(self.canvas.coords('left_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('left_handle', points)
        points = self.add_difference(self.canvas.coords('right_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('right_handle', points)

        points = self.add_difference(self.canvas.coords('upper_left_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_left_handle', points)
        points = self.add_difference(self.canvas.coords('lower_left_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_left_handle', points)
        points = self.add_difference(self.canvas.coords('upper_right_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_right_handle', points)
        points = self.add_difference(self.canvas.coords('lower_right_handle'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_right_handle', points)

        points = self.add_difference(self.canvas.coords('upper_left_line'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_left_line', points)
        points = self.add_difference(self.canvas.coords('upper_right_line'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('upper_right_line', points)
        points = self.add_difference(self.canvas.coords('left_upper_line'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('left_upper_line', points)
        points = self.add_difference(self.canvas.coords('left_lower_line'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('left_lower_line', points)
        points = self.add_difference(self.canvas.coords('lower_left_line'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_left_line', points)
        points = self.add_difference(self.canvas.coords('lower_right_line'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('lower_right_line', points)
        points = self.add_difference(self.canvas.coords('right_lower_line'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('right_lower_line', points)
        points = self.add_difference(self.canvas.coords('right_upper_line'), diff_x=diff_x, diff_y=diff_y)
        self.canvas.coords('right_upper_line', points)

        self.area_move_start_coords = event
