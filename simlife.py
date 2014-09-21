import pygame
from options import options
import random
from life import Creature, bud, breed
from utils import Point, compare_color
from simutils import cell_to_canvas, choose_neighbor, choose_specific_neighbor, choose_empty_neighbor, find_or_make_empty_space, kill, rgb_to_pycolor, rect_from_location
from globals import g


# do not edit! added by PythonBreakpoints
from pudb import set_trace as _breakpoint


class SimCreature(Creature):

    """Base class for creatures for simple_sim"""

    def subclass_init(self, loc=None):
        if loc:
            self.location = loc
        else:
            self.location = self.random_point()
        self.rect = None

    def random_point(self):
        x = int(random.random() * options.xcells)
        y = int(random.random() * options.ycells)
        return Point(x=x, y=y)

    def step(self):
        raise NotImplementedError

    def draw(self):
        cx, cy = cell_to_canvas(self.location)
        possible_rect = self.draw_subclass(cx, cy)
        if possible_rect:
            self.rect = possible_rect
            g.changed_rects.append(self.rect)

    def move(self, newloc):
        self.erase()
        old_loc = self.location
        self.location = newloc
        g.creatures[newloc] = self
        del g.creatures[old_loc]

    def draw_subclass(self):
        raise NotImplementedError

    def erase(self):
        mycell = rect_from_location(self.location)
        background_fill = self.draw_over(mycell)
        g.changed_rects.append(background_fill)

    def draw_over(self, rect):
        return g.surface.fill(g.background_color, rect)

    def kill(self):
        self.erase()
        del self


class SimWall(SimCreature):

    """Doesn't move or change. Not alive - just a wall"""
    traits = []

    def subclass_init(self, loc):
        super(SimWall, self).subclass_init(loc)
        self.color = pygame.Color("#663300")
        self.rect = 0

    def step(self):
        pass

    def draw_subclass(self, cx, cy):
        size = (options.cellsize)
        rect = g.surface.fill(self.color, (cx, cy, size, size,))
        return rect


class VolitileCreature(SimCreature):

    def step(self):
        self.step_subclass()


class SimHerbivore(VolitileCreature):

    """
    Eats SimPlants, breeds if it can,
    buds if it gets to maximum energy.
    Ability to eat the plants is based on how similar the colors are
    Draw's a circle, size is determined by energy
    """
    traits = ['r', 'g', 'b']
    start_energy = 45.0
    max_energy = 250.0
    metabolism = 5.0
    min_breed_energy = 60.0
    breed_energy_loss = 40.0
    min_bud_energy = 100.0
    bud_energy_loss = 50.0
    max_age = 350
    mutation_rate = 1.0

    def subclass_init(self, loc=None):
        super(SimHerbivore, self).subclass_init(loc)
        self.energy = self.start_energy
        self.color = rgb_to_pycolor(self.r, self.g, self.b)
        self.age = 0

    def step_subclass(self):
        self.energy -= self.metabolism
        self.age = self.age + 1
        if self.energy <= 0 or self.age > self.max_age:
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
                    self.energy = min(self.max_energy, self.energy)
                    kill(neighbor_space)
                    neighbor = None

            elif type(neighbor) == self.__class__:
                if self.energy > self.min_breed_energy:
                    child_space = find_or_make_empty_space(
                        self.location, victims=[SimPlant])

                    if child_space:
                        self.energy = self.energy - self.breed_energy_loss
                        g.creatures[child_space] = breed(
                            self, neighbor, loc=child_space)

        if not neighbor:  # either was empty or got eaten.
            # move there
            self.move(neighbor_space)

        if self.energy > self.min_bud_energy:  # SOO MUCH ENERGY! GONNA BUD
            child_space = find_or_make_empty_space(self.location, victims=[SimPlant])
            if child_space:
                g.creatures[child_space] = bud(self, loc=child_space)
                self.energy == self.energy - self.bud_energy_loss

    def draw_subclass(self, cx, cy):
        self.erase()
        size = int((self.energy / self.max_energy) *
                   (options.cellsize / 2) + options.cellsize / 2)
        offset = (options.cellsize - size) // 2
        cx = offset + cx
        cy = offset + cy
        ellipse = pygame.draw.ellipse(g.surface, self.color,
                                     (cx, cy, size, size), )
        return ellipse

    def draw_over(self, rect):
        return pygame.draw.ellipse(g.surface, g.background_color, rect)


class SimPlant(VolitileCreature):

    """
    slowly gains energy up to a maximum,
    each turn it will choose a nearby space and
    bud/breed to it if possible
    Has a color which is genetically inherited
    """
    traits = ['r', 'g', 'b']
    max_energy = 70
    breed_energy = 10

    def subclass_init(self, loc=None):
        super(SimPlant, self).subclass_init(loc)
        self.energy = 0
        self.color = rgb_to_pycolor(self.r, self.g, self.b)
        self.size = -1
        self.surrounded = False

    def step_subclass(self):
        self.energy = min(self.energy + 1, self.max_energy)

        if self.energy > 20:
            if not self.surrounded or random.random() < 0.05:
                self.breed()

    def breed(self):

        neighbor_space = choose_empty_neighbor(self.location)
        if neighbor_space:

            # try to breed sexually - look for a mate in a neighboring loc
            mate_space = choose_specific_neighbor(self.location, SimPlant)
            if mate_space:
                self.surrounded = False
                self.energy = self.energy - self.breed_energy
                g.creatures[neighbor_space] = breed(
                    self, g.creatures[mate_space], loc=neighbor_space)
        else:
            self.surrounded = True

    def draw_subclass(self, cx, cy):
        newsize = min(
            options.cellsize, options.cellsize * self.energy / self.max_energy + 1)
        if not self.rect or self.size != newsize or g.time % 5 == 0:
            self.size = newsize
            offset = (options.cellsize - newsize) / 2
            cx = offset + cx
            cy = offset + cy
            rect = g.surface.fill(self.color, (cx, cy,  newsize,  newsize))
            return rect
