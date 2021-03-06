from options import options
import random
from globals import g
from utils import Point
from math import floor
import pygame
from utils import compare_color



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
    left_edge = apoint.x <= 0
    right_edge = apoint.x > options.xcells - 1
    top_edge = apoint.y <= 0
    bottom_edge = apoint.y > options.ycells - 1

    if not top_edge:
        possible_neighbors.append(Point(apoint.x, apoint.y - 1))
        if not right_edge:
            possible_neighbors.append(Point(apoint.x + 1, apoint.y - 1))
        if not left_edge:
            possible_neighbors.append(Point(apoint.x - 1, apoint.y - 1))

    if not bottom_edge:
        possible_neighbors.append(Point(apoint.x, apoint.y + 1))
        if not right_edge:
            possible_neighbors.append(Point(apoint.x + 1, apoint.y + 1))
        if not left_edge:
            possible_neighbors.append(Point(apoint.x - 1, apoint.y + 1))

    if not right_edge:
        possible_neighbors.append(Point(apoint.x + 1, apoint.y))

    if not left_edge:
        possible_neighbors.append(Point(apoint.x - 1, apoint.y))

    return possible_neighbors

def chance_to_eat(color1, color2):
    similarity = compare_color(color1, color2)
    return 0.4 * (similarity**4 + 0.05) # small constant chance to eat

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

def choose_specific_neighbor(apoint, neighbor_cls):
    possible_neighbors = neighbors(apoint)
    while possible_neighbors:
        choice = random.choice(range(len(possible_neighbors)))
        choice_spot = possible_neighbors[choice]
        chosen_creature = g.creatures.get(choice_spot, None)
        if type(chosen_creature) == neighbor_cls:
            return choice_spot
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

def rect_from_location(apoint):
    cx, cy = cell_to_canvas(apoint)
    return (cx, cy,  options.cellsize,  options.cellsize)

def hsl_to_pycolor(h, s, l):
    color = pygame.Color(0,0,0,0)
    color.hsla = (h, s, l, 0)
    return color

def space_empty(apoint):
    if apoint in g.creatures:
            return False
    return True

def kill(apoint):
    if apoint in g.creatures:
        g.creatures[apoint].kill()
        del g.creatures[apoint]

