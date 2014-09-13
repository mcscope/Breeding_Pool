from options import options
import random
from globals import g
from utils import Point
from math import floor



def cell_to_canvas(apoint):
    return (apoint.x * options.cellsize, apoint.y * options.cellsize)

def canvas_to_cell(x,y):
    return Point(*(floor(x/options.cellsize), floor(y/ options.cellsize)))


def valid_cell(apoint):
    valid =  0 <= apoint.x <= options.xcells and \
        0 <= apoint.y <= options.ycells
    return valid


def neighbors(apoint):
    possible_neighbors = []
    if apoint.x > 0:
        possible_neighbors.append(Point(apoint.x - 1, apoint.y))

    if apoint.y > 0:
        possible_neighbors.append(Point(apoint.x, apoint.y - 1))

    if apoint.x < options.xcells:
        possible_neighbors.append(Point(apoint.x + 1, apoint.y))

    if apoint.y < options.ycells:
        possible_neighbors.append(Point(apoint.x, apoint.y + 1))
    return possible_neighbors


def choose_neighbor(apoint):
    possible_neighbors = neighbors(apoint)
    return random.choice(possible_neighbors)


def choose_empty_neighbor(apoint):
    possible_neighbors = neighbors(apoint)
    while possible_neighbors:
        choice = random.choice(range(len(possible_neighbors)))
        if space_empty(possible_neighbors[choice]):
            return possible_neighbors[choice]
        del possible_neighbors[choice]
    return None


def find_or_make_empty_space(apoint, victims=[]):
    empty_neighbor = choose_empty_neighbor(apoint)
    if empty_neighbor:
        return empty_neighbor
    for victim_type in victims:
        possible_neighbors = neighbors(apoint)
        while possible_neighbors:
            curspace = possible_neighbors.pop()
            if g.creatures[curspace].__class__ == victim_type:
                kill(curspace)
                return curspace

    return None



def space_empty(apoint):
    if apoint in g.creatures:
            return False
    return True

def kill(apoint):
    if apoint in g.creatures:
        g.creatures[apoint].kill()
        del g.creatures[apoint]

