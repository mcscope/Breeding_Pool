from Tkinter import *
from options import options
from simutils import  canvas_to_cell, kill
from simlife import SimPlant, SimHerbivore, SimWall
from functools import partial
from globals import g



class SimpleSim():

    def __init__(self):
        self.root = Tk()
        self.RUN = False

        self.frame = Frame(bg="black")
        self.frame.pack()
        self.TEXT = "Simple life simulation"

        g.canvas = Canvas(self.frame,
                          highlightthickness=0,
                          bg="#4E2F2F",
                             width=(options.xcells + 1) * options.cellsize,
                             height=(options.ycells + 1) * options.cellsize)
        g.canvas.pack()

        g.creatures = {}
        self.start()

        self.root.mainloop()

    def start(self):
        self.time = 0
        self.RUN = True

        self.bindings = {
            "<Button-1>": partial(self.clickSpawn, SimPlant),
            "<Button-2>": partial(self.clickSpawn, SimHerbivore),
            "<B3-Motion>": partial(self.clickSpawn, SimWall),
            "w": partial(self.clickSpawn, SimWall),
        }
        for button, func in self.bindings.iteritems():
            g.canvas.bind(button, func)
        self.run()

    def run(self):
        if self.RUN is True:
            if self.time % 10 == 0:
                print len(g.creatures)
            self.time += 1
            for creature in g.creatures.values():
                creature.step()
            self.paint()
            self.root.after(10, self.run)

    def end(self):
        self.RUN = False
        for binding in self.bindings.keys():
            g.canvas.unbind(binding)

    def clickSpawn(self,  spawn_class, event):
        click_loc = canvas_to_cell(event.x, event.y)
        kill(click_loc)
        g.creatures[click_loc] = spawn_class(loc=click_loc)

    def paint(self):
        for creature in g.creatures.values():
            creature.draw()

app = SimpleSim()
