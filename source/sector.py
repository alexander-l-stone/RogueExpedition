import tdl
from .system import System
from random import *
import math
from .constants import *
from .generate import SystemGenerator

#TODO: Test this file

class Sector:

    def __init__(self, name, sector_type, x, y, width, height, sysnames={}):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.name = name
        self.sector_type = sector_type
        self.systemlist = []
        self.centerx = self.width//2
        self.centery = self.height//2
        self.sysnames = sysnames
        self.objlist = []
        self.generator = SystemGenerator()

    def generate(self):
        if len(self.systemlist) == 0:
            namenumber = randrange(0,len(system_names)-1)
            name = system_names[namenumber]
            new_x = randrange(self.x*self.width, (self.x+1)*self.width)
            new_y = randrange(self.y*self.height, (self.y+1)*self.height)
            if system_names[namenumber] in self.sysnames:
                self.sysnames[name] += 1
            else:
                self.sysnames[name] = 0
            if self.sysnames[name] < len(greek_numbers)-1:
                new_system = System(greek_numbers[self.sysnames[name]] + " " + system_names[namenumber], new_x, new_y, generate=False, sector=self)
                self.generator.generate(new_system)
                self.systemlist.append(new_system)
            else:
                new_system = System(str(system_names[namenumber]) + " " + str(self.sysnames[name]), new_x, new_y, generate=False, sector=self)
                self.generator.generate(new_system)
                self.systemlist.append(new_system)
        numsystems = randrange(int(self.height*self.width*0.002), int(self.height*self.width*0.01))
        i = 2
        while i < numsystems:
            new_x = randrange(self.x*self.width, (self.x+1)*self.width)
            new_y = randrange(self.y*self.height, (self.y+1)*self.height)
            empty = True
            for solar in self.systemlist:
                if (new_x == solar.x) and (new_y == solar.y):
                    empty = False
                    break
            if empty:
                namenumber = randrange(0,len(system_names)-1)
                name = system_names[namenumber]
                result = self.sysnames.get(name)
                if result == None:
                    self.sysnames[name] = 0
                else:
                    self.sysnames[name] += 1
                if self.sysnames[name] < len(greek_numbers)-1:
                    new_system = System(greek_numbers[self.sysnames[name]] + " " + system_names[namenumber], new_x, new_y, generate=False, sector=self)
                    self.generator.generate(new_system)
                    self.systemlist.append(new_system)
                else:
                    new_system = System(str(system_names[namenumber]) + " " + str(self.sysnames[name]), new_x, new_y, generate=False, sector=self)
                    self.generator.generate(new_system)
                    self.systemlist.append(new_system)
                i += 1

    # def generate_name():
    #     listLength = len(syllables)

    def draw(self, console, topx, topy, sw, sh):
        for system in self.systemlist:
            if (system.x-topx > 0) and (system.y-topy > 0) and (system.x-topx < sw) and (system.y-topy < sh):
                console.draw_char(system.x-topx, system.y-topy, system.star.char, system.star.color)
        for obj in self.objlist:
            obj.draw(console, topx, topy, sw, sh)


    def sector_clear(self, console, topx, topy, sw, sh):
        self.clear(console, topx, topy, sw, sh)
        for node in self.adjacent_sectors:
            node.clear(console, topx, topy, sw, sh)

    def clear(self, console, topx, topy, sw, sh):
        for system in self.systemlist:
            if (system.x-topx > 0) and (system.y-topy > 0) and (system.x-topx < sw) and (system.y-topy < sh):
                console.draw_char(system.x-topx, system.y-topy, ' ')
        for obj in self.objlist:
            obj.draw(console, topx, topy, sw, sh)
