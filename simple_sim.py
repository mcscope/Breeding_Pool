import pygame
from options import options
from simple_sim.simutils import canvas_to_cell, kill
from simple_sim.simlife import SimPlant, SimHerbivore, SimWall
from functools import partial
from globals import g


class SimpleSim():

    def __init__(self):
        pygame.init()
        self.RUN = False

        g.width = int((options.xcells + 1) * options.cellsize)
        g.height = int((options.ycells + 1) * options.cellsize)
        g.background_color = pygame.Color("#444444")
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        if options.fullscreen:
            flags = flags | pygame.FULLSCREEN
        g.surface = pygame.display.set_mode((g.width, g.height), flags)
        g.surface.set_alpha(None)
        g.draw = True
        g.drawstep = 1
        self.reset()
        self.start()


    def start(self):
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
            u'w': self.plantWall,
            u'd': self.toggleDraw,
            u'-': partial(self.change_step,-3) ,
            u'=': partial(self.change_step,3),


        }
        self.run()

    def run(self):
        while self.RUN is True:
            ev = pygame.event.poll()    # Look for any event
            if ev:
                self.handle_event(ev)

            g.time += 1
            if g.time % 10 == 0:
                print "%s: %s" % (g.time,len(g.creatures))
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
        g.time=0
        g.creatures = {}
        g.changed_rects = []
        pygame.display.update(g.surface.fill(g.background_color))

    def plantWall(self):
        pos = pygame.mouse.get_pos()
        self.placeAt(pos, SimWall)

    def toggleDraw(self):
        g.draw = not g.draw

    def change_step(self, delta):
        g.drawstep = max(1, g.drawstep + delta)

    def placeAt(self, position,spawn_class):
        click_loc = canvas_to_cell(*(position))
        kill(click_loc)
        g.creatures[click_loc] = spawn_class(loc=click_loc)


    def clickSpawn(self, event):
        if event.button not in self.mouse_bindings:
            return
        spawn_class = self.mouse_bindings[event.button]
        self.placeAt(event.pos, spawn_class)

    def handle_keys(self, event):
        if event.unicode in self.key_bindings:
            self.key_bindings[event.unicode]()

    def paint(self):
        if not g.draw:
            return
        if g.time % g.drawstep != 0:
            return
        for creature in g.creatures.values():
            creature.draw()
        pygame.display.update(g.changed_rects)
        g.changed_rects = []

if __name__ == "__main__" and __package__ is None:
    __package__ = "simple_sim"
    SimpleSim()
