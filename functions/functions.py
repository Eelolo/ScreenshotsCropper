
def rgb_to_tk_color(rgb):
    return "#%02x%02x%02x" % rgb


def get_round_rect_points(x1, y1, x2, y2, radius=10):
    points = [
        x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1,
        x2, y1, x2, y1 + radius, x2, y1 + radius, x2, y2 - radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2,
        x1 + radius, y2, x1 + radius, y2, x1, y2, x1, y2 - radius,
        x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1
    ]

    return points


def get_center_pos(x0, y0, x1, y1):
    x = int(x0 - (x0 - x1) / 2)
    y = int(y0 - (y0 - y1) / 2)

    return x, y
