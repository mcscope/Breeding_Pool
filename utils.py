from collections import namedtuple
from numpy.linalg import norm
from numpy import array
from options import options



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



def compare_color(rgb1, rgb2):
    rgb1 =  normalize_rgb(rgb1)
    rgb2 =  normalize_rgb(rgb2)
    total_difference = sum([abs(c1 - c2) for c1,c2 in zip(rgb1, rgb2)])
    max_distance = 256 * 3
    similarity = (max_distance - total_difference)/ (max_distance)
    return similarity


def normalize_rgb(rgb):
    return [color % 256 for color in rgb]

def normalize(in_array):
    norm_scalar =  norm(in_array)
    if norm_scalar == 0:
        return in_array

    return in_array / norm_scalar

def normalize_to_window(in_array):

    in_array = in_array % array([options.width, options.height])
    in_array = array([max(in_array[0], 0),
                    max(in_array[1], 0) ])
    return in_array
