from Tkinter import *
from options import options
import random
from life import Creature, bud, breed
from utils import rgb_to_hex, Point, compare_color
from simutils import cell_to_canvas, choose_neighbor, space_empty, find_or_make_empty_space, kill
from globals import g


class SimCreature(Creature):
    """Base class for creatures for simple_sim"""

    def subclass_init(self, loc=None):
        if loc:
            self.location = loc
        else:
            self.location = self.random_point()
        self.shape = None

    def random_point(self):
        x = int(random.random() * options.xcells)
        y = int(random.random() * options.ycells)
        return Point(x=x, y=y)

    def step(self):
        raise NotImplementedError

    def draw(self):
        cx, cy = cell_to_canvas(self.location)
        self.draw_subclass(cx, cy)

    def draw_subclass(self):
        raise NotImplementedError

    def kill(self):
        if self.shape:
            g.canvas.delete(self.shape)
        del self


class SimWall(SimCreature):
    """Doesn't move or change. Not alive - just a wall"""
    traits = []

    def step(self):
        pass

    def draw_subclass(self, cx, cy):
        if not self.shape:
            size = (options.cellsize)
            self.shape = g.canvas.create_rectangle(
                cx, cy, cx + size, cy + size, fill='brown', outline="black")


class SimHerbivore(SimCreature):
    """
    Eats SimPlants, breeds if it can,
    buds if it gets to maximum energy.
    Ability to eat the plants is based on how similar the colors are
    Draw's a circle, size is determined by energy
    """
    traits = ['r', 'g', 'b']

    def subclass_init(self, loc=None):
        super(SimHerbivore, self).subclass_init(loc)
        self.energy = 40
        self.color = rgb_to_hex(self.r, self.g, self.b)
        self.age = 0

    def step(self):
        self.energy -= 3
        self.age = self.age + 1
        if self.energy <= 0 or self.age > 300:
            kill(self.location)
            return

        neighbor_space = choose_neighbor(self.location)
        neighbor = g.creatures.get(neighbor_space)
        if neighbor:
            if type(neighbor) == SimPlant:
                color_similarity = compare_color([self.r, self.g, self.b],
                                                 [neighbor.r, neighbor.g, neighbor.b])
                if random.random() < color_similarity:
                    self.energy = self.energy + neighbor.energy
                    kill(neighbor_space)
                    neighbor = None

            elif type(neighbor) == self.__class__:
                might_have_space = True
                while self.energy > 70 and might_have_space:
                    child_space = find_or_make_empty_space(
                        self.location, victims=[SimPlant])

                    if child_space:
                        self.energy = self.energy - 20
                        g.creatures[child_space] = breed(
                            self, neighbor, loc=child_space)
                    else:
                        might_have_space = False

        if not neighbor:  # either was empty or got eaten.
            old_loc = self.location
            self.location = neighbor_space
            g.creatures[neighbor_space] = self
            del g.creatures[old_loc]

        self.energy = min(200, self.energy)
        if self.energy == 200:  # SOO MUCH ENERGY! GONNA BUD
            child_space = find_or_make_empty_space(self.location, victims=[SimPlant])
            if child_space:
                g.creatures[child_space] = bud(self, loc=child_space)
                self.energy == 100



    def draw_subclass(self, cx, cy):
        if self.shape:
            g.canvas.delete(self.shape)
        size = self.energy / 70.0 * (options.cellsize)
        offset = (options.cellsize - size) / 2
        cx = offset + cx
        cy = offset + cy
        self.shape = g.canvas.create_oval(
            cx, cy, cx + size, cy + size, fill=self.color)


class SimPlant(SimCreature):
    """
    slowly gains energy up to a maximum,
    each turn it will choose a nearby space and
    bud/breed to it if possible
    Has a color which is genetically inherited
    """
    traits = ['r', 'g', 'b']

    def subclass_init(self, loc=None):
        super(SimPlant, self).subclass_init(loc)
        self.energy = 0
        self.color = rgb_to_hex(self.r, self.g, self.b)
        self.size = 0

    def step(self):
        self.energy = min(self.energy + 1, 40)

        if self.energy > 20:

            neighbor_space = choose_neighbor(self.location)
            if neighbor_space and space_empty(neighbor_space):
                self.energy = self.energy - 20

                 ##try to breed sexually - look for a mate in a neighboring loc
                mate_space = choose_neighbor(self.location)
                if space_empty(mate_space):
                    g.creatures[neighbor_space] = bud(
                        self, loc=neighbor_space)

                elif type(g.creatures[mate_space]) == self.__class__:
                    g.creatures[neighbor_space] = breed(
                        self, g.creatures[mate_space], loc=neighbor_space)

    def draw_subclass(self, cx, cy):
        newsize = min(options.cellsize, self.energy // 5 + 1)
        if newsize != self.size:  # if our size has changed.
            self.size = newsize
            if self.shape:
                g.canvas.delete(self.shape)
            offset = (options.cellsize - newsize) / 2
            cx = offset + cx
            cy = offset + cy
            self.shape = g.canvas.create_rectangle(
                cx, cy, cx + newsize, cy + newsize, fill=self.color, outline=self.color)
