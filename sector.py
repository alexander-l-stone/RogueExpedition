import tdl
from system import System
from random import *
import math
from constants import *
from generate import SystemGenerator

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

    def generate_name():
        listLength = len(syllables)

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

    def to_json(self):
        height = self.height
        width = self.width
        x = self.x
        y = self.y
        name = self.name
        sector_type = self.sector_type
        sysnames = self.sysnames
        systemlist = []
        objlist = []
        for system in self.systemlist:
            systemlist.append(system.to_json())
        for obj in self.objlist:
            with open('test.log', 'a') as f:
                f.write('\n')
                f.write(str(obj) + '\n')
                f.closed
            objlist.append(obj.to_json())

        json_data = {
            'height' : height,
            'width' : width,
            'x' : x,
            'y' : y,
            'name' : name,
            'sector_type' : sector_type,
            'sysnames' : sysnames,
            'systemlist' : systemlist,
            'objlist' : objlist
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        from system import System
        from ship import Ship
        height = json_data.get('height')
        width = json_data.get('width')
        x = json_data.get('x')
        y = json_data.get('y')
        name = json_data.get('name')
        sector_type = json_data.get('sector_type')
        sysnames = json_data.get('sysnames')
        systemlist = json_data.get('systemlist')
        objlist = json_data.get('objlist')


        sector = Sector(name, sector_type, x, y, height, width, sysnames=sysnames)
        for system in systemlist:
            new_system = System.from_json(system)
            new_system.sector = sector
            sector.systemlist.append(new_system)
        for obj_data in objlist:
            if obj_data.get('type') == 'ship':
                new_ship = Ship.from_json(obj_data)
                sector.objlist.append(new_ship)
        return sector
