from collections import namedtuple
Point = namedtuple("Point", ('x', 'y'))


class dictobj(dict):

    def __init__(self, _entries=None, **kw):
        if _entries is None:
            _entries = {}
        self.update(_entries)
        self.update(kw)

    def to_json(self):
        return self

    def to_dict(self):
        return dict(self.iteritems())

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError, attr

    def __setattr__(self, attr, val):
        self[attr] = val

    def copy(self):
        return dictobj(self)


def rgb_to_hex(r, g, b):
    rgb = [r, g, b]
    rgb = normalize_rgb(rgb)
    return '#%02x%02x%02x' % tuple(rgb)

def compare_color(rgb1, rgb2):
    rgb1 =  normalize_rgb(rgb1)
    rgb2 =  normalize_rgb(rgb2)
    total_difference = sum([abs(c1 - c2) for c1,c2 in zip(rgb1, rgb2)])
    max_distance = 256 * 3
    similarity = (max_distance - total_difference)/ (max_distance)
    return similarity**3 + 0.05  # d20 to eat it even if the colors don't match

def normalize_rgb(rgb):
    return [color % 256 for color in rgb]
