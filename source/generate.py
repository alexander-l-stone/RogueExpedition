import random
from random import *
from .system import Star, System, Planet, Ring, Wormhole

import math
#FIXME: Put generators here when import errors are resolved
#TODO: Test this file
class SystemGenerator:
    def __init__(self):
        #TODO: Add and use a seed for the rng
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
        system.hyperlimit = Ring('#', (255,100,100), hyperradius, 'hyperradius', system.name + ' Hyperlimit')

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
                zone[0:46] = ['hot']*(46+1-0)
                zone[47:80] = ['bio']*(80+1-47)
                zone[81:100] = ['cold']*(100+1-81)
                zone[101:560] = ['gas']*(560+1-101)
                zone[561:706] = ['ice']*(706+1-561)
            elif system.star.stellar_type == 'Yellow-White':
                zone = [None]*601
                zone[0:18] = ['hot']*(18+1-0)
                zone[19:36] = ['bio']*(36+1-19)
                zone[37:50]  = ['cold']*(50+1-37)
                zone[51:260] = ['gas']*(260+1-51)
                zone[261:600] = ['ice']*(600+1-261)
            elif system.star.stellar_type == 'Yellow':
                zone = [None]*601
                zone[0:10] = ['hot']*(10+1-0)
                zone[11:24] = ['bio']*(24+1-11)
                zone[25:32] = ['cold']*(32+1-25)
                zone[33:166] = ['gas']*(166+1-33)
                zone[167:600] = ['ice']*(600+1-167)
            elif system.star.stellar_type == 'Orange':
                zone = [None]*501
                zone[0:4] = ['hot']*(4+1-0)
                zone[5:10] = ['bio']*(10+1-5)
                zone[11:18] = ['cold']*(18+1-11)
                zone[19:76] = ['gas']*(76+1-19)
                zone[77:500] = ['ice']*(500+1-77)
            elif system.star.stellar_type == 'Red':
                zone = [None]*409
                zone[0:10] = ['hot']*(10+1-0)
                zone[11:14] = ['bio']*(14+1-11)
                zone[15:18] = ['cold']*(18+1-15)
                zone[19:36] = ['gas']*(36+1-19)
                zone[37:408] = ['ice']*(408+1-37)
            elif system.star.stellar_type == 'Red Dwarf':
                zone = [None]*409
                zone[0:12] = ['cold']*(12+1-0)
                zone[13:22] = ['gas']*(22+1-13)
                zone[23:408] = ['ice']*(408+1-23)
            else:
                zone = ['empty']
            # with open('debug.log', 'a+') as debug:
            #     debug.write('\n----')
            #     debug.write('\n' + system.name)
            #     debug.write('\n' + str(zone))
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
        # with open('debug.log', 'a+') as debug:
        #         debug.write("\nRadius: " + str(radius) + "| Zone: " + str(planet_zone))
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
            elif planet_zone == 'ice':
                body = Planet('0', (randrange(0,100), randrange(0,255), randrange(0,255)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Liquid Giant', system.name + ' ' + str(i), system=system  )
            else:
                return
        else:
            if planet_zone == 'hot':
                body = Planet('o', (randrange(50,150), randrange(200,255), randrange(50,150)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Greenhouse', system.name + ' ' + str(i), system=system  )
            elif planet_zone == 'bio':
                body = Planet('0', (randrange(0,15), randrange(255), randrange(0,15)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Super-Terran', system.name + ' ' + str(i), system=system  )
            elif planet_zone == 'cold':
                value = randrange(50,100)
                body = Planet('o', (value, value//2, 0), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Barren', system.name + ' ' + str(i)  )
            elif planet_zone == 'gas':
                body = Planet('O', (randrange(0,255), randrange(0,255), randrange(0,255)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Gas Giant', system.name + ' ' + str(i), system=system  )
            elif planet_zone == 'ice':
                body = Planet('0', (randrange(0,100), randrange(0,255), randrange(0,255)), radius, int(radius*math.cos(random_angle)), int(radius*math.sin(random_angle)), 'Liquid Giant', system.name + ' ' + str(i), system=system  )
            else:
                return
        system.planetlist.append(body)
        if isinstance(body, Ring):
            return
        # print(str(body.name) + ' ' + str(body.planet_type) + ' ' + str(body.moonlist))
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
            moonradius = randrange(6,22)//2
        else:
            moonradius = randrange(9,21)//3
        while nummoons > 0:
            random_angle = math.radians(randrange(0,360))
            if body.planet_type == 'Liquid Giant' or body.planet_type == 'Frozen':
                moon = Planet('o', (randrange(0,150), randrange(100,255), randrange(255)), moonradius, int(moonradius*math.cos(random_angle)), int(moonradius*math.sin(random_angle)), 'Frozen',body.name + " " + moonname[5-nummoons])
                body.moonlist.append(moon)
                moonradius += randrange(3,11)
            elif body.planet_type == 'Hot' or body.planet_type == 'Greenhouse':
                moon = Planet('o', (255, randrange(0,255), randrange(0,150)), moonradius, int(moonradius*math.cos(random_angle)), int(moonradius*math.sin(random_angle)), 'Hot', body.name + " " + moonname[5-nummoons])
                body.moonlist.append(moon)
                moonradius += randrange(3,8)
            else:
                value = randrange(50,100)
                moon = Planet('o', (value, value//2, 0), moonradius, int(moonradius*math.cos(random_angle)), int(moonradius*math.sin(random_angle)), 'Barren', body.name + " " + moonname[5-nummoons])
                body.moonlist.append(moon)
                moonradius += randrange(3,8)
            nummoons -= 1
        if len(body.moonlist) < 1:
            body.planet_limit = Ring('#', (255,255,255), randrange(7,12), 'Planetary Limit', body.name + " Limit")
            #append sensor information to the planet
            body.sensor_information['optical'] = {0:'This planet has no moons'}
        elif len(body.moonlist) >= 1:
            last_moon = body.moonlist[-1]
            body.planet_limit = Ring('#', (255,255,255), randrange(last_moon.radius + 4, last_moon.radius + 5), 'Planetary Limit', body.name + " Limit")
            #append sensor information to the planet
            if len(body.moonlist == 1):
                body.sensor_information['optical'] = {0:'This planet has 1 moon'}
            else:
                body.sensor_information['optical'] = {0:"""This planet has {len(body.moonlist)} moons"""}
