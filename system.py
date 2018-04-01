import tdl
import math
import random
from random import *
from display import GameObject

#Generate tag is legacy code
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
        if generate:
            #FIXME: Remove the below when this workaround is no longer needed
            sg = SystemGenerator()
            sg.generate(self)

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

    def to_json(self):
        name = self.name
        x = self.x
        y = self.y
        sector = self.sector.name
        if self.owner == None:
            owner = None
        else:
            owner = self.owner.name
        explored = self.explored
        star = self.star.to_json()
        planetlist = []
        for planet in self.planetlist:
            planetlist.append(planet.to_json())
        systemlist = []
        for sobj in self.system_objects:
            systemlist.append(sobj.to_json())
        objlist = []
        for obj in self.objlist:
            objlist.append(obj.to_json())
        hyperlimit = self.hyperlimit.to_json()

        json_data = {
            'name' : name,
            'x' : x,
            'y' : y,
            'sector' : sector,
            'owner' : owner,
            'explored' : explored,
            'star' : star,
            'planetlist' : planetlist,
            'hyperlimit' : hyperlimit,
            'objectlist' : objlist,
            'systemlist' : systemlist,
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        x = json_data.get('x')
        y = json_data.get('y')
        sector = json_data.get('sector')
        owner = json_data.get('owner')
        explored = json_data.get('explored')
        hyperlimit = json_data.get('hyperlimit')
        planetlist = json_data.get('planetlist')
        systemlist = json_data.get('systemlist')
        objectlist = json_data.get('objectlist')

        system = System(name, x, y, generate=False, sector=sector, owner=owner)
        for planet in planetlist:
            new_planet = Planet.from_json(planet)
            new_planet.system = system
            system.planetlist.append(new_planet)
        for sysobj_data in systemlist:
            if sysobj_data.get('type') == 'wormhole':
                new_wormhole = Wormhole.from_json(sysobj_data)
                system.system_objects.append(new_wormhole)
        for obj_data in objectlist:
            if obj_data.get('type') == 'ship':
                new_ship = Ship.from_json(obj_data)
                system.objlist.append(obj_data)
        return system

class Star(GameObject):
    def __init__(self, char, color, x, y, name, stellar_type, mass):
        GameObject.__init__(self, char, color, x, y)
        self.name = name
        self.stellar_type = stellar_type
        self.mass = mass
        self.explored = False

    def to_json(self):
        char = self.char
        color = self.color
        x = self.x
        y = self.y
        name = self.name
        stellar_type = self.stellar_type
        mass = self.mass
        explored = self.explored

        json_data = {
            'char' : char,
            'color' : color,
            'x' : x,
            'y' : y,
            'name' : name,
            'stellar_type' : stellar_type,
            'mass' : mass,
            'explored' : explored
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        char = json_data.get('char')
        color = json_data.get('color')
        x = json_data.get('x')
        y = json_data.get('y')
        name = json_data.get('name')
        stellar_type = json_data.get('stellar_type')
        mass = json_data.get('mass')
        explored = json_data.get('explored')

        star = Star(char, color, x, y, name, stellar_type, mass)
        star.explored = explored
        return star

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
        if moonlist == None:
            self.moonlist = []
        else:
            self.moonlist = moonlist
        self.objlist = []
        self.planet_limit = None

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

    def to_json(self):
        name = self.name
        radius = self.radius
        char = self.char
        color = self.color
        x = self.x
        y = self.y
        explored = self.explored
        planet_type = self.planet_type
        if self.owner == None:
            owner = None
        else:
            owner = self.owner.name
        if self.colony == None:
            colony = None
        else:
            colony = self.colony.to_json()
        system = self.system.name
        moonlist = []
        for moon in self.moonlist:
            moonlist.append(moon.to_json())
        planet_limit = self.planet_limit.to_json
        objectlist = []
        for obj in self.objlist:
            objectlist.append(obj)
        json_data = {
            'name' : name,
            'radius' : radius,
            'char' : char,
            'color' : color,
            'x' : x,
            'y' : y,
            'explored' : explored,
            'planet_type' : planet_type,
            'moonlist' : moonlist,
            'colony' : colony,
            'planet_limit' : planet_limit,
            'objectlist' : objectlist
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        radius = json_data.get('radius')
        char = json_data.get('char')
        x = json_data.get('x')
        y = json_data.get('y')
        explored = json_data.get('explored')
        planet_type = json_data.get('planet_type')
        moonlist = json_data.get('moonlist')
        colony = json_data.get('colony')
        planet_limit = json_data.get('planet_limit')
        owner = json_data.get('owner')
        objectlist = json_data.get('objectlist')

        planet = Planet(char, color, radius, x, y, planet_type, name, moonlist=None, system=system, owner=owner)
        for moon in moonlist:
            new_moon = Planet.from_json(moon)
            new_moon.system = planet
            planet.moonlist.append(new_moon)
        for obj_data in objectlist:
            if obj_data.get('type') == 'ship':
                new_ship = Ship.from_json(obj_data)
                planet.objlist.append(new_ship)
        return planet

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

    def to_json(self):
        json_data = {
        'char' : self.char,
        'name' : self.name,
        'color' : self.color,
        'radius' : self.radius,
        'planet_type' : self.planet_type,
        'explored' : self.explored
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        char = json_data.get(char)
        name = json_data.get(name)
        color = json_data.get(color)
        radius = json_data.get(radius)
        planet_type = json_data.get(planet_type)
        explored = json_data.get(explored)

        ring = Ring(char, color, radius, planet_type, name)
        ring.explored = explored
        return ring

class Wormhole(GameObject):
    def __init__(self, char, color, radius, system=None, destination=None):
        random_angle = math.radians(randrange(0,360))
        self.radius = radius
        x = int(self.radius*math.cos(random_angle))
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

    def to_json(self):
        if self.destination == None:
            destination_data = None
        else:
            destination_data = (self.destination.name, self.destination.system.name)
        json_data = {
        'type' : 'wormhole',
        'char' : self.char,
        'color' : self.color,
        'radius' : self.radius,
        'x' : self.x,
        'y' : self.y,
        'system' : self.system.name,
        'destination' : destination_data
        }

        return json_data

    #returns self, note that location and destination are set to be strings
    @staticmethod
    def from_json(json_data):
        from ship import Ship
        x = json_data.get('x')
        y = json_data.get('y')
        char = json_data.get('char')
        color = json_data.get('color')
        radius = json_data.get('radius')
        system = json_data.get('system')
        destination = json_data.get('destination')

        wormhole = Wormhole(char, color, radius)
        wormhole.x = x
        wormhole.y = y
        wormhole.system = system
        wormhole.destination = destination
        return wormhole

#legacy code and currently unused.
class SystemGenerator:
    def __init__(self):
        pass

    def generate(self, system):
        system.star = self.generate_star(system)
        self.generate_system(system)
        self.generate_hyperlimit(system)

    def generate_hyperlimit(self, system):
        if len(system.planetlist) == 0:
            hyperradius = 5*system.star.mass
        else:
            last = len(system.planetlist) - 1
            hyperradius = max(5*system.star.mass, system.planetlist[last].radius + 2*system.star.mass)
        system.hyperlimit = Ring('#', (50,0,0), hyperradius, 'hyperradius', system.name + ' Hyperlimit')

    def generate_star(self, system):
        dieroll = randrange(0,100)
        if dieroll < 5:
            rg = randrange(0,50)
            return Star('O', (rg,rg,255), 0, 0, system.name, 'Blue Giant', randrange(10,20))
        elif dieroll < 10:
            rgb = randrange(220,255)
            return Star('O', (rgb, rgb, rgb), 0, 0, system.name, 'White', randrange(2,6))
        elif dieroll < 20:
            rg = randrange(220,255)
            b = randrange(120,170)
            return Star('O', (rg,rg,b), 0, 0, system.name, 'Yellow-White', randrange(2,6))
        elif dieroll < 30:
            rg = randrange(220,255)
            return Star('O', (rg,rg,50), 0, 0, system.name, 'Yellow', randrange(2,6))
        elif dieroll < 50:
            r = randrange(220,255)
            g = r//2
            return Star('O', (r,g,0), 0, 0, system.name, 'Orange', randrange(2,6))
        elif dieroll < 70:
            r = randrange(180,220)
            return Star('O', (r,0,0), 0, 0, system.name, 'Red', randrange(2, 6))
        elif dieroll < 80:
            r = randrange(130,170)
            return Star('O', (r,0,0), 0, 0, system.name, 'Red Dwarf', randrange(0,3))
        elif dieroll < 90:
            rgb = randrange(220,255)
            return Star('O', (rgb,rgb,rgb), 0, 0, system.name, 'White Dwarf', randrange(0,3))
        else:
            r = randrange(230,255)
            return Star('O', (r,0,0), 0, 0, system.name, 'Red Giant', randrange(10,20))

    def generate_system(self, system):
        if not system.star.stellar_type == 'Blue Giant' or not system.star.stellar_type == 'White Dwarf' or not system.star.stellar_type == 'Red Giant':
            radius1 = randrange(8, 13)
            radius2 = randrange(min(15,max(16,radius1+2)), min(17,radius1+9))
            random_angle = randrange(0,360)
            num_planets = randrange(-1, 10)
            dieroll = 0
            if system.star.stellar_type == 'White':
                zone = [None]*707
                zone[0:46] ='hot'
                zone[47:80] = 'bio'
                zone[82:100] = 'cold'
                zone[101:560] = 'gas'
                zone[561:706] = 'ice'
            elif system.star.stellar_type == 'Yellow-White':
                zone = [None]*601
                zone[0:18] = 'hot'
                zone[19:36] = 'bio'
                zone[37:50]  = 'cold'
                zone[51:260] = 'gas'
                zone[261:600] = 'ice'
            elif system.star.stellar_type == 'Yellow':
                zone = [None]*601
                zone[0:10] ='hot'
                zone[11:24] = 'bio'
                zone[25:32] = 'cold'
                zone[33:166] = 'gas'
                zone[167:600] = 'ice'
            elif system.star.stellar_type == 'Orange':
                zone = [None]*501
                zone[0:4] = 'hot'
                zone[5:10] = 'bio'
                zone[11:18] = 'cold'
                zone[19:76] = 'gas'
                zone[77:500] = 'ice'
            elif system.star.stellar_type == 'Red':
                zone = [None]*409
                zone[0:10] = 'hot'
                zone[11:14] = 'bio'
                zone[15:18] = 'cold'
                zone[19:36] = 'gas'
                zone[37:408] = 'ice'
            elif system.star.stellar_type == 'Red Dwarf':
                zone = [None]*409
                zone[0:12] = 'cold'
                zone[13:22] = 'gas'
                zone[23:408] = 'ice'
            else:
                zone = ['empty']
            if num_planets > 0:
                if len(zone) > radius1:
                    planet_zone = zone[radius1]
                else:
                    planet_zone = 'empty'
                self.generate_planet(system, planet_zone, radius1, 1)
            if num_planets > 1:
                if len(zone) > radius2:
                    planet_zone = zone[radius2]
                else:
                    planet_zone = 'empty'
                self.generate_planet(system, planet_zone, radius2, 2)
            if num_planets > 2:
                i = 3
                while i < num_planets:
                    ##("---")
                    ##("Radius 1: " + str(radius1))
                    ##("Radius 2: " + str(radius2))
                    ##("I: " + str(i-2))
                    radius = radius2 - radius1
                    radius *= 2
                    radius *= i-2
                    radius += radius1
                    ##("Radius: " + str(radius))
                    if len(zone) > radius and radius > 0:
                        planet_zone = zone[radius]
                    else:
                        planet_zone = 'empty'
                    if radius > 0:
                        self.generate_planet(system, planet_zone, radius, i)
                    i+=1
            for planet in system.planetlist:
                if planet.name == 'Empty Space':
                    system.planetlist.remove(planet)
        else:
            return

    def generate_system_objects(self, system):
        system_objects_chance = randrange(1,101)
        num_objects = 0
        if system_objects_chance > 50:
            num_objects = 1
        elif system_objects_chance > 75:
            num_objects = 2
        elif system_objects_chance > 90:
            num_objects = 3
        elif system_objects_chance > 98:
            num_objects = 4
        for i in range(num_objects):
            if system.hyperlimit.radius - 3 > 5:
                randradius = randrange(2, system.hyperlimit.radius-1)
                for planet in system.planetlist:
                    if planet.radius == randradius:
                        randradius += 1
                    new_wormhole = Wormhole('X', (200, 66, 244), randradius, system)
                    system.system_objects.append(new_wormhole)

    def generate_planet(self, system, planet_zone, radius, i):
        dieroll = randrange(0,100)
        random_angle = math.radians(randrange(0,360))
        body = Ring(' ', (0,0,0), 0, 'Empty Space', 'Empty Space')
        if dieroll < 3:
            pass
        elif dieroll < 6:
            if planet_zone == 'hot' or planet_zone == 'bio' or planet_zone == 'gas' or planet_zone == 'cold':
                body = Ring('*', (70,45,15), radius, 'Asteroid Belt', system.name + ' Asteroid Belt ' + str(i))
            else:
                body = Ring('*', (140,255,255), radius, 'Ice Belt', system.name + ' Ice Belt ' + str(i))
        elif dieroll < 26:
            if planet_zone == 'hot':
                body = Planet('o', (255, randrange(0,255), randrange(0,150)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Hot', system.name + ' ' + str(i), system=system )
            if planet_zone == 'ice':
                body = Planet('o', (randrange(0,150), randrange(100,255), randrange(255)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Frozen', system.name + ' ' + str(i),system=system )
            else:
                value = randrange(50,100)
                body = Planet('o', (value, value//2, 0), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Barren', system.name + ' ' + str(i), system=system )
        elif dieroll < 76:
            if planet_zone == 'hot':
                body = Planet('o', (randrange(50,150), randrange(200,255), randrange(50,150)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Greenhouse', system.name + ' ' + str(i), system=system)
            elif planet_zone == 'bio':
                body = Planet('o', (randrange(0,15), randrange(255), randrange(0,15)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Terran' ,system.name + ' ' + str(i), system=system)
            elif planet_zone == 'cold':
                value = randrange(50,100)
                body = Planet('o', (value, value//2, 0), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Barren', system.name + ' ' + str(i), system=system )
            elif planet_zone == 'gas':
                body = Planet('O', (randrange(0,255), randrange(0,255), randrange(0,255)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Gas Giant', system.name + ' ' + str(i), system=system  )
            else:
                body = Planet('0', (randrange(0,100), randrange(0,255), randrange(0,255)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Liquid Giant', system.name + ' ' + str(i), system=system  )
        else:
            if planet_zone == 'hot':
                body = Planet('o', (randrange(50,150), randrange(200,255)), randrange(50,150), radius, int(radius1*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Greenhouse', system.name + ' ' + str(i), system=system  )
            elif planet_zone == 'bio':
                body = Planet('0', (randrange(0,15), randrange(255), randrange(0,15)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Super-Terran', system.name + ' ' + str(i), system=system  )
            elif planet_zone == 'cold':
                value = randrange(50,100)
                body = Planet('o', (value, value//2, 0), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Barren', system.name + ' ' + str(i)  )
            elif planet_zone == 'gas':
                body = Planet('O', (randrange(0,255), randrange(0,255), randrange(0,255)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Gas Giant', system.name + ' ' + str(i), system=system  )
            else:
                body = Planet('0', (randrange(0,100), randrange(0,255), randrange(0,255)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Liquid Giant', system.name + ' ' + str(i), system=system  )
        system.planetlist.append(body)
        moonchance = randrange(0,100)
        if body.planet_type == 'Barren' or body.planet_type == 'Terran':
            moonchance += -35
        elif body.planet_type == 'Super-Terran':
            moonchance += 0
        elif body.planet_type == 'Frozen' or body.planet_type == 'Hot':
            moonchance += -15
        elif body.planet_type == 'Liquid Giant':
            moonchance += 35
        elif body.planet_type == 'Gas Giant':
            moonchance += 50
        elif body.planet_type == 'Greenhouse':
            moonchance += -35
        nummoons = 0
        if moonchance < 1:
            nummoons = 0
        elif moonchance < 56:
            nummoons = 1
        elif moonchance < 86:
            nummoons = 2
        elif moonchance < 106:
            nummoons = 3
        elif moonchance < 127:
            nummoons = 4
        else:
            nummoons = 5
        if isinstance(body, Ring):
            nummoons = 0
        moonname = ['A', 'B', 'C', 'D', 'E']
        if body.planet_type == 'Gas Giant' or body.planet_type == 'Liquid Giant':
            moonradius = randrange(1,11)//2
        else:
            moonradius = randrange(1,11)//3
        while nummoons > 0:
            random_angle = math.radians(randrange(0,360))
            if body.planet_type == 'Liquid Giant' or body.planet_type == 'Frozen':
                moon = Planet('o', (randrange(0,150), randrange(100,255), randrange(255)), moonradius, int(moonradius*math.cos(random_angle)), int(moonradius*math.sin(random_angle)), 'Frozen',body.name + " " + moonname[5-nummoons])
                body.moonlist.append(moon)
                moonradius += randrange(1,11)
            elif body.planet_type == 'Hot' or body.planet_type == 'Greenhouse':
                moon = Planet('o', (255, randrange(0,255), randrange(0,150)), moonradius, int(moonradius*math.cos(random_angle)), int(moonradius*math.sin(random_angle)), 'Hot', body.name + " " + moonname[5-nummoons])
                body.moonlist.append(moon)
                moonradius += randrange(1,6)
            else:
                value = randrange(50,100)
                moon = Planet('o', (value, value//2, 0), moonradius, int(moonradius*math.cos(random_angle)), int(moonradius*math.sin(random_angle)), 'Barren', body.name + " " + moonname[5-nummoons])
                body.moonlist.append(moon)
                moonradius += randrange(1,6)
            nummoons -= 1
        if len(body.moonlist) < 1:
            body.planet_limit = Ring('#', (255,255,255), randrange(5,11), 'Planetary Limit', body.name + " Limit")
        elif len(body.moonlist) >= 1:
            last_moon = body.moonlist[-1]
            body.planet_limit = Ring('#', (255,255,255), randrange(last_moon.radius + 2, last_moon.radius + 5), 'Planetary Limit', body.name + " Limit")
