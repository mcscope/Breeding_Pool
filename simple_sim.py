import pygame
from options import options
from simutils import canvas_to_cell, kill
from simlife import SimPlant, SimHerbivore, SimWall
from functools import partial
from globals import g


# do not edit! added by PythonBreakpoints
from pudb import set_trace as _breakpoint


class SimpleSim():

    def __init__(self):
        pygame.init()
        self.RUN = False

        g.width = int((options.xcells + 1) * options.cellsize)
        g.height = int((options.ycells + 1) * options.cellsize)
        g.background_color = pygame.Color("#4E2F2F")
        g.surface = pygame.display.set_mode((g.width, g.height))

        g.creatures = {}
        self.start()


    def start(self):
        self.time = 0
        self.RUN = True

        self.bindings = {
        "MouseButtonDown": self.clickSpawn,
        "KeyDown": self.handle_keys
        }
        self.mouse_bindings = {
            1: SimPlant,
            3: SimHerbivore,
            2: SimWall,
        }
        self.key_bindings = {
            u'q': self.end,
            u'r': self.reset,
        }
        self.run()

    def run(self):
        while self.RUN is True:
            ev = pygame.event.poll()    # Look for any event
            if ev:
                self.handle_event(ev)

            if self.time % 10 == 0:
                print len(g.creatures)
            self.time += 1
            for creature in g.creatures.values():
                creature.step()
            self.paint()

    def handle_event(self, event):
        if event == pygame.QUIT:
            self.end()
        event_name = pygame.event.event_name(event.type)

        if event_name in self.bindings:
            self.bindings[event_name](event)


    def end(self):
        self.RUN = False
        pygame.quit()

    def reset(self):
        self.time=0
        g.creatures = {}

    def clickSpawn(self, event):
        if event.button not in self.mouse_bindings:
            return
        spawn_class = self.mouse_bindings[event.button]
        click_loc = canvas_to_cell(*(event.pos))
        kill(click_loc)
        g.creatures[click_loc] = spawn_class(loc=click_loc)

    def handle_keys(self, event):
        if event.unicode in self.key_bindings:
            self.key_bindings[event.unicode]()

    def paint(self):
        g.surface.fill(g.background_color)
        for creature in g.creatures.values():
            creature.draw()

        pygame.display.flip()


SimpleSim()
