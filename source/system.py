import tdl
import math
import random
from random import *
from .display import GameObject
# from .generate import SystemGenerator

#Generate tag is legacy code
#TODO: Test this file
class System:
    def __init__(self, name, x, y, generate=True, sector=None, owner=None):
        self.name = name
        self.star = None
        self.planetlist = []
        self.x = x
        self.y = y
        self.explored = False
        self.owner = None
        self.system_objects = []
        self.objlist = []
        self.sector = sector
        self.sensor_information = {}
        self.hyperlimit = Ring('#', (255, 100, 100), 5, 'hyperradius', self.name + ' Hyperlimit')

    def draw(self, console, topx, topy, sw, sh):
        self.hyperlimit.draw(console, topx, topy, sw, sh)
        if len(self.planetlist) > 0:
            for planet in self.planetlist:
                planet.draw(console, topx, topy, sw, sh)
        if len(self.system_objects) > 0:
            for thing in self.system_objects:
                thing.draw(console, topx, topy, sw, sh)
        if len(self.objlist) > 0:
            for obj in self.objlist:
                obj.draw(console, topx, topy, sw, sh)
        self.star.draw(console, topx, topy, sw, sh)

    def clear(self, console, topx, topy, sw, sh):
        self.star.clear(console, topx, topy, sw, sh)
        if len(self.planetlist) > 0:
            for planet in self.planetlist:
                planet.clear(console, topx, topy, sw, sh)
        if len(self.system_objects) > 0:
            for thing in self.system_objects:
                thing.clear(console, topx, topy, sw, sh)
        if len(self.objlist) > 0:
            for obj in self.objlist:
                obj.clear(console, topx, topy, sw, sh)
        self.hyperlimit.clear(console, topx, topy, sw, sh)


class Star(GameObject):
    def __init__(self, char, color, x, y, name, stellar_type, mass):
        GameObject.__init__(self, char, color, x, y)
        self.name = name
        self.stellar_type = stellar_type
        self.mass = mass
        self.explored = False
        self.sensor_information = { 
            'thermal': { 0: 'This Star is a normal temperature for its Spectral Class.'},
            'electromagnetic' : {0: 'This Star is experiencing normal electromagnetic activity.'},
            'gravity': {0: 'This Star is have a normal gravitational effect.'}
            }


class Planet(GameObject):
    def __init__(self, char, color, radius, x, y, planet_type, name, moonlist=None, system=None, owner=None):
        GameObject.__init__(self, char, color, x, y)
        self.name = name
        self.radius = radius
        self.explored = False
        self.planet_type = planet_type
        self.owner = owner
        self.colony = None
        self.system = system
        self.moonlist = []
        self.objlist = []
        self.planet_limit = None
        self.sensor_information = {}

    def draw(self, console, topx, topy, sw, sh):
        if (self.x-topx > 0) and (self.y-topy > 0) and (self.x-topx < sw) and (self.y-topy < sh):
            if self.owner == None:
                console.draw_char(self.x-topx, self.y-topy, self.char, self.color, bg=None)
            else:
                console.draw_char(self.x-topx, self.y-topy, self.char, self.color, bg=(self.owner.red, self.owner.green, self.owner.blue))

    def planet_draw(self, console, topx, topy, sw, sh):
        self.planet_limit.draw(console, topx, topy, sw, sh)
        if (0 - topx > 0) and (0 - topy > 0) and (0 - topx < sw) and (0 - topy < sh):
            if self.owner == None:
                console.draw_char(0-topx, 0-topy, self.char, self.color, bg=None)
            else:
                console.draw_char(0-topx, 0-topy, self.char, self.color, bg=(self.owner.red, self.owner.green, self.owner.blue))
        for moon in self.moonlist:
            moon.draw(console, topx, topy, sw, sh)
        for obj in self.objlist:
            obj.draw(console,topx, topy, sw, sh)

    def planet_clear(self, console, topx, topy, sw, sh):
        self.planet_limit.clear(console, topx, topy, sw, sh)
        if (0 - topx > 0) and (0 - topy > 0) and (0 - topx < sw) and (0 - topy < sh):
            console.draw_char(0-topx, 0-topy, ' ', self.color, bg=(0,0,0))
        for moon in self.moonlist:
            moon.clear(console, topx, topy, sw, sh, clearbg=(0,0,0))
        for obj in self.objlist:
            obj.clear(console, topx, topy, sw, sh, clearbg=(0,0,0))


class Ring:
    def __init__(self, char, color, radius, ring_type, name):
        self.color = color
        self.radius = radius
        self.name = name
        self.char = char
        self.planet_type = ring_type
        self.explored = False
        self.moonlist = []

    def draw(self, console, topx, topy, sw, sh):
        for theta in range(0,360):
            x = int(self.radius*math.cos(theta))
            y = int(self.radius*math.sin(theta))
            if (x-topx > 0) and (y-topy > 0) and (x-topx < sw) and (y-topy < sh):
                console.draw_char(x-topx, y-topy, self.char, self.color)

    def clear(self, console, topx, topy, sw, sh, clearbg = None):
        for theta in range(0,360):
            x = int(self.radius*math.cos(theta))
            y = int(self.radius*math.sin(theta))
            if (x-topx > 0) and (y-topy > 0) and (x-topx < sw) and (y-topy < sh):
                console.draw_char(x-topx, y-topy, ' ')


class Wormhole(GameObject):
    def __init__(self, char, color, radius, system=None, destination=None):
        random_angle = math.radians(randrange(0,360))
        self.radius = radius
        x = int(self.radius*math.cos(random_angle))
        y = int(self.radius*math.sin(random_angle))
        GameObject.__init__(self, char, color, x, y)
        self.system = system
        if not self.system == None:
            self.system.system_objects.append(self)
        self.destination = destination

    def generate_destination(self, galaxy, sector):
        randx = randrange(-10, +10)
        randy = randrange(-10, +10)
        target_sector = galaxy.get_sector(sector, randx, randy)
        target_system = choice(target_sector.systemlist)
        randradius = randrange(2, target_system.hyperlimit.radius-1)
        for planet in target_system.planetlist:
            if planet.radius == randradius:
                randradius += 1
        new_wormhole = Wormhole("X", (200,66,244), randradius, target_system, destination=self)
        target_system.system_objects.append(new_wormhole)
        self.destination = new_wormhole
        return self.destination

    #destination is a tuple of (system_name, self_name)
    def find_destination(self, galaxy, destination):
        dest_system = None
        dest_wormhole = None
        for key,value in galaxy.sectorlist.items():
            for system in value.systemlist:
                if system.name == destination[1]:
                    dest_system = system
                    break
            if not dest_system == None:
                break
        if dest_system == None:
            self.generate_destination(galaxy, self.system.sector)
        else:
            for sysobj in dest_system.system_objects:
                if isinstance(sysobj, Wormhole):
                    if sysobj.destination[0] == self.name:
                        dest_wormhole = sysobj
                        break
        if dest_wormhole == None:
            self.generate_destination(galaxy, self.system.sector)
        else:
            self.destination = dest_wormhole
            dest_wormhole.destination = self
        return self.destination

    def draw(self, console, topx, topy, sw, sh):
        if (self.x-topx > 0) and (self.y-topy > 0) and (self.x-topx < sw) and (self.y-topy < sh):
            console.draw_char(self.x-topx, self.y-topy, self.char, self.color, bg=None)

    def clear(self, console, topx, topy, sw, sh, clearbg=None):
        if (self.x-topx > 0) and (self.y-topy > 0) and (self.x-topx < sw) and (self.y-topy < sh):
            console.draw_char(self.x-topx, self.y-topy, ' ', bg=clearbg)


