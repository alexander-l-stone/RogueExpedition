import tdl
from display import GameObject
from system import *
from sector import Sector
import math
from component import *
from galaxy import *
from timer import Timer

class Ship(GameObject):

    def __init__(self, char, color, x, y, name, model, size, timer, ui=None, componentlist=None, system=None, isPlayer=False, faction=None):
        super(Ship, self).__init__(char, color, x, y)
        self.name = name
        self.model = model
        self.sensor_range = 1
        self.cargo_list = {}
        self.size = size
        self.faction = faction
        if componentlist == None:
            self.componentlist = []
            self.power_max = 0
            self.current_power = 0
            self.cargo_max = 0
            self.current_cargo = 0
        else:
            self.componentlist = componentlist
            for module in self.componentlist:
                if isinstance(module, Reactor):
                    self.power_max += module.power_produced
                    self.current_power += module.power_produced
                elif isinstance(module, Capacitor):
                    self.power_max += module.power_amount
                elif isinstance(module, CargoBay):
                    self.cargo_max += module.cargo_amount
                elif isinstance(module, Sensor):
                    if module.sensor_range > self.sensor_range:
                        self.sensor_range = module.sensor_range
        self.location = system
        self.player = isPlayer
        if isPlayer:
            self.ui = ui
        else:
            self.ui = Panel(100,100,20,20, 50)
        self.alert = 'green'
        self.current_clock = Timer(minutes=timer.minutes)

    def calculate_statistics(self):
        self.power_max = 0
        self.cargo_max = 0
        self.sensor_range = 1
        for module in self.componentlist:
            if isinstance(module, Reactor):
                if module.active and not module.damaged:
                    self.power_max += module.power_produced
            elif isinstance(module, Capacitor):
                if module.active and not module.damaged:
                    self.power_max += module.power_amount
            elif isinstance(module, CargoBay):
                if module.active and not module.damaged:
                    self.cargo_max += module.cargo_amount
            elif isinstance(module, Sensor):
                if module.active and not module.damaged:
                    if module.sensor_range > self.sensor_range:
                        self.sensor_range = module.sensor_range
        self.current_power = min(self.current_power, self.power_max)

    def activate(self, ui):
        recalculate = False
        for module in self.componentlist:
            if module.damaged:
                recalculate = True
            module_activity = module.active
            module_type, module_power = module.activate(self, self.ui)
            self.current_power -= module_power
            if not module_activity == module.active:
                recalculate = True
        for component in self.componentlist:
            if isinstance(component, Reactor):
                module_type = component.activate(self.current_power, self.ui)[0]
                if module_type == 'reactor':
                    if not component.fuel_type.symbol == "y":
                        added_power = component.produce_power(ui, self)
                        if self.power_max > self.current_power + added_power:
                            self.current_power += added_power
                        else:
                            self.current_power = self.power_max
                    else:
                        if isinstance(self.location, System) or isinstance(self.location, Planet):
                            added_power = component.produce_power(ui, self)
                            if self.power_max > self.current_power + added_power:
                                self.current_power += added_power
                            else:
                                self.current_power = self.power_max
        if recalculate:
            self.calculate_statistics()


    def attemptJump(self, clock):
        if not isinstance(self.location, System):
            if isinstance(self.location, Planet):
                if self.player:
                    self.ui.message("Too close to planet to jump", "helm")
            else:
                return False
        else:
            distance_from_star = math.pow((math.pow(self.x, 2)) + (math.pow(self.y, 2)), 1/2)
            if distance_from_star >= self.location.hyperlimit.radius:
                if self.player:
                    self.ui.message("Jumping to hyperspace",  'helm')
                if self.x > 0 and self.y == 0:
                    self.x = self.location.x + 1
                    self.y = self.location.y
                elif self.x == 0 and self.y > 0:
                    self.x = self.location.x
                    self.y = self.location.y + 1
                elif self.x < 0 and self.y == 0:
                    self.x = self.location.x - 1
                    self.y = self.location.y
                elif self.x == 0 and self.y < 0:
                    self.x = self.location.x
                    self.y = self.location.y - 1
                elif self.x < 0 and self.y < 0:
                    theta = math.degrees(math.atan(self.x/self.y))
                    if theta > 90 - 22.5:
                        self.x = self.location.x - 1
                        self.y = self.location.y
                    elif theta < 0 + 22.5:
                        self.x = self.location.x
                        self.y = self.location.y - 1
                    else:
                        self.x = self.location.x - 1
                        self.y = self.location.y - 1
                elif self.x > 0 and self.y > 0:
                    theta = math.degrees(math.atan(self.x/self.y))
                    if theta > 90 - 22.5:
                        self.x = self.location.x + 1
                        self.y = self.location.y
                    elif theta < 0 + 22.5:
                        self.x = self.location.x
                        self.y = self.location.y + 1
                    else:
                        self.x = self.location.x + 1
                        self.y = self.location.y + 1
                elif self.x < 0 and self.y > 0:
                    theta = math.degrees(math.atan(self.x/self.y))
                    if theta < -90 + 22.5:
                        self.x = self.location.x - 1
                        self.y = self.location.y
                    elif theta > 0 - 22.5:
                        self.x = self.location.x
                        self.y = self.location.y + 1
                    else:
                        self.x = self.location.x - 1
                        self.y = self.location.y + 1
                elif self.x > 0 and self.y < 0:
                    theta = math.degrees(math.atan(self.x/self.y))
                    if theta > 0 - 22.5:
                        self.x = self.location.x
                        self.y = self.location.y - 1
                    elif theta < -90 + 22.5:
                        self.x = self.location.x + 1
                        self.y = self.location.y
                    else:
                        self.x = self.location.x + 1
                        self.y = self.location.y - 1
                self.location = self.location.sector
            else:
                if self.player:
                    self.ui.message("Jump failed, too close to star", 'helm')

    def get_thrust(self):
        thrust = 0
        size = 0
        for component in self.componentlist:
            size += component.size
            if isinstance(component, Engine):
                thrust += component.check_thrust(self.ui, self)
        return thrust/size

    def attemptMove(self, galaxy, dx, dy):
        entering_planet = False
        if self.location == None:
            self.move(dx, dy)
            return True
        elif isinstance(self.location, System):
            successful_move = True
            if (self.location.star.x == self.x+dx) and (self.location.star.y == self.y+dy):
                successful_move = False
            else:
                if len(self.location.planetlist) > 0:
                    for planet in self.location.planetlist:
                        if (isinstance(planet, Planet)):
                            if (planet.x == self.x+dx) and (planet.y == self.y + dy):
                                successful_move = False
                                self.location = planet
                                entering_planet = True
                                if dx == -1 and dy == 0:
                                    self.x = 1*self.location.planet_limit.radius
                                    self.y = 0*self.location.planet_limit.radius
                                    return True
                                elif dx == -1 and dy == -1:
                                    self.x = int((math.pow(2,1/2)/2)*self.location.planet_limit.radius)
                                    self.y = int((math.pow(2,1/2)/2)*self.location.planet_limit.radius)
                                    return True
                                elif dx == 0 and dy == 1:
                                    self.x = 0*self.location.planet_limit.radius
                                    self.y = -1*self.location.planet_limit.radius
                                    return True
                                elif dx == 1 and dy == 1:
                                    self.x = -1*int((math.pow(2,1/2)/2)*self.location.planet_limit.radius)
                                    self.y = -1*int((math.pow(2,1/2)/2)*self.location.planet_limit.radius)
                                    return True
                                elif dx == 1 and dy == 0:
                                    self.x = -1*self.location.planet_limit.radius
                                    self.y = 0*self.location.planet_limit.radius
                                    return True
                                elif dx == 1 and dy == -1:
                                    self.x = -1*int((math.pow(2,1/2)/2)*self.location.planet_limit.radius)
                                    self.y = int((math.pow(2,1/2)/2)*self.location.planet_limit.radius)
                                    return True
                                elif dx == 0 and dy == -1:
                                    self.x = 0*self.location.planet_limit.radius
                                    self.y = 1*self.location.planet_limit.radius
                                    return True
                                elif dx == -1 and dy == 1:
                                    self.x = int((math.pow(2,1/2)/2)*self.location.planet_limit.radius)
                                    self.y = -1*int((math.pow(2,1/2)/2)*self.location.planet_limit.radius)
                                    return True
                                break
                if len(self.location.system_objects) > 0:
                    for obj in self.location.system_objects:
                        if (obj.x == self.x + dx) and (obj.y == self.y + dy):
                            if isinstance(obj, Wormhole):
                                if obj.destination == None:
                                    exit_wormhole = obj.generate_destination(galaxy, self.location.sector)
                                else:
                                    exit_wormhole = obj.destination
                                self.location = exit_wormhole.system
                                if self.player:
                                    self.ui.message("Entering " + self.location.name, 'helm')
                                self.x = exit_wormhole.x + dx
                                self.y = exit_wormhole.y + dy
                                successful_move = False
                                return True
                            else:
                                successful_move = False
                                return False
                        else:
                            successful_move = True
            if successful_move and not entering_planet:
                self.move(dx, dy)
                if int(math.pow(math.pow(max(self.location.star.x, self.x) - min(self.location.star.x, self.x),2) + math.pow(max(self.location.star.y, self.y) - min(self.location.star.y, self.y), 2), 1/2)) <= self.sensor_range:
                    self.location.explored = True
                return True
            else:
                return False
        elif isinstance(self.location, Planet):
            successful_move = True
            if self.x+dx == 0 and self.y+dy == 0:
                successful_move = False
            else:
                if len(self.location.moonlist) > 0:
                    for moon in self.location.moonlist:
                        if isinstance(moon, Planet):
                            if moon.x == self.x+dx and moon.y == self.y + dy:
                                successful_move = False
            if successful_move:
                distance_from_planet = math.pow((math.pow(self.x, 2)) + (math.pow(self.y, 2)), 1/2)
                if distance_from_planet >= self.location.planet_limit.radius + 1:
                    if self.x > 0 and self.y == 0:
                        self.x = self.location.x + 1
                        self.y = self.location.y
                    elif self.x == 0 and self.y > 0:
                        self.x = self.location.x
                        self.y = self.location.y + 1
                    elif self.x < 0 and self.y == 0:
                        self.x = self.location.x - 1
                        self.y = self.location.y
                    elif self.x == 0 and self.y < 0:
                        self.x = self.location.x
                        self.y = self.location.y - 1
                    elif self.x < 0 and self.y < 0:
                        theta = math.degrees(math.atan(self.x/self.y))
                        if theta > 90 - 22.5:
                            self.x = self.location.x - 1
                            self.y = self.location.y
                        elif theta < 0 + 22.5:
                            self.x = self.location.x
                            self.y = self.location.y - 1
                        else:
                            self.x = self.location.x - 1
                            self.y = self.location.y - 1
                    elif self.x > 0 and self.y > 0:
                        theta = math.degrees(math.atan(self.x/self.y))
                        if theta > 90 - 22.5:
                            self.x = self.location.x + 1
                            self.y = self.location.y
                        elif theta < 0 + 22.5:
                            self.x = self.location.x
                            self.y = self.location.y + 1
                        else:
                            self.x = self.location.x + 1
                            self.y = self.location.y + 1
                    elif self.x < 0 and self.y > 0:
                        theta = math.degrees(math.atan(self.x/self.y))
                        if theta < -90 + 22.5:
                            self.x = self.location.x - 1
                            self.y = self.location.y
                        elif theta > 0 - 22.5:
                            self.x = self.location.x
                            self.y = self.location.y + 1
                        else:
                            self.x = self.location.x - 1
                            self.y = self.location.y + 1
                    elif self.x > 0 and self.y < 0:
                        theta = math.degrees(math.atan(self.x/self.y))
                        if theta > 0 - 22.5:
                            self.x = self.location.x
                            self.y = self.location.y - 1
                        elif theta < -90 + 22.5:
                            self.x = self.location.x + 1
                            self.y = self.location.y
                        else:
                            self.x = self.location.x + 1
                            self.y = self.location.y - 1
                    self.location = self.location.system
                    return True
                else:
                    self.move(dx, dy)
                    return True
            else:
                return False
        elif isinstance(self.location, Sector):
            successful_move = True
            entering_system = False
            if len(self.location.systemlist) > 0:
                for system in self.location.systemlist:
                    if (system.x == self.x+dx) and (system.y == self.y + dy):
                        entering_system = True
                        if self.player:
                            self.ui.message("Entering " + system.name, 'helm')
                        self.location = system
                        has_wormhole = False
                        for sysobj in self.location.system_objects:
                            if isinstance(sysobj, Wormhole):
                                has_wormhole = True
                        if has_wormhole:
                            if self.player:
                                self.ui.message("", 'helm')
                                self.ui.message("I am detecting a gravitational anomaly.", 'science')
                            for msg in self.ui.msgs:
                                print(msg)
                        if dx == -1 and dy == 0:
                            self.x = 1*self.location.hyperlimit.radius
                            self.y = 0*self.location.hyperlimit.radius
                            return True
                        elif dx == -1 and dy == -1:
                            self.x = int((math.pow(2,1/2)/2)*self.location.hyperlimit.radius)
                            self.y = int((math.pow(2,1/2)/2)*self.location.hyperlimit.radius)
                            return True
                        elif dx == 0 and dy == 1:
                            self.x = 0*self.location.hyperlimit.radius
                            self.y = -1*self.location.hyperlimit.radius
                            return True
                        elif dx == 1 and dy == 1:
                            self.x = -1*int((math.pow(2,1/2)/2)*self.location.hyperlimit.radius)
                            self.y = -1*int((math.pow(2,1/2)/2)*self.location.hyperlimit.radius)
                            return True
                        elif dx == 1 and dy == 0:
                            self.x = -1*self.location.hyperlimit.radius
                            self.y = 0*self.location.hyperlimit.radius
                            return True
                        elif dx == 1 and dy == -1:
                            self.x = -1*int((math.pow(2,1/2)/2)*self.location.hyperlimit.radius)
                            self.y = int((math.pow(2,1/2)/2)*self.location.hyperlimit.radius)
                            return True
                        elif dx == 0 and dy == -1:
                            self.x = 0*self.location.hyperlimit.radius
                            self.y = 1*self.location.hyperlimit.radius
                            return True
                        elif dx == -1 and dy == 1:
                            self.x = int((math.pow(2,1/2)/2)*self.location.hyperlimit.radius)
                            self.y = -1*int((math.pow(2,1/2)/2)*self.location.hyperlimit.radius)
                            return True
                        break
            if successful_move and not entering_system:
                self.move(dx, dy)
                lessthanx = self.x < self.location.x*self.location.width
                lessthany = self.y < self.location.y*self.location.height
                greaterthanx = self.x > (self.location.x+1)*self.location.width-1
                greaterthany = self.y > (self.location.y+1)*self.location.height-1
                if lessthanx and lessthany:
                    self.location = galaxy.get_sector(self.location, -1, -1)
                    return True
                elif lessthanx and greaterthany:
                    self.location = galaxy.get_sector(self.location, -1, 1)
                    return True
                elif greaterthanx and lessthany:
                    self.location = galaxy.get_sector(self.location, 1, -1)
                    return True
                elif greaterthanx and greaterthany:
                    self.location = galaxy.get_sector(self.location, 1, 1)
                    return True
                elif greaterthanx and not lessthany and not greaterthany:
                    self.location = galaxy.get_sector(self.location, 1, 0)
                    return True
                elif lessthanx and not lessthany and not greaterthany:
                    self.location = galaxy.get_sector(self.location, -1, 0)
                    return True
                elif greaterthany and not lessthanx and not greaterthanx:
                    self.location = galaxy.get_sector(self.location, 0, 1)
                    return True
                elif lessthany and not lessthanx and not greaterthanx:
                    self.location = galaxy.get_sector(self.location, 0, -1)
                    return True
                return True
            else:
                return False

    def to_json(self):
        name = self.name
        x = self.x
        y = self.y
        char = self.char
        color = self.color
        model = self.model
        cargolist = []
        for key,val in self.cargo_list:
            new_cargo = key.to_json
            cargolist.append((new_cargo, val))
        size = self.size
        componentlist = []
        for obj in self.componentlist:
            componentlist.append(obj.to_json())
        location = self.location.name
        player = self.player
        alert = self.alert
        clock = self.current_clock.to_json()
        faction = self.faction.name

        json_data = {
            'type' : 'ship',
            'name' : name,
            'x' : x,
            'y' : y,
            'char' : char,
            'color' : color,
            'model' : model,
            'cargolist' : cargolist,
            'size' : size,
            'componentlist' : componentlist,
            'location' : location,
            'player' : player,
            'alert' : alert,
            'clock' : clock,
            'faction' : faction
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        x = json_data.get('x')
        y = json_data.get('y')
        char = json_data.get('char')
        color = json_data.get('color')
        model = json_data.get('model')
        cargolist = json_data.get('cargolist')
        size = json_data.get('size')
        componentlist = json_data.get('componentlist')
        location = json_data.get('location')
        player = json_data.get('player')
        alert = json_data.get('alert')
        clock = json_data.get('clock')
        faction = json_data.get('faction')

        ship = Ship(char, color, x, y, name, model, size, clock, ui=None, componentlist=componentlist, isPlayer=player, faction=faction)
        ship.location = location
        ship.alert = alert
        for cargo in cargolist:
            ship.cargolist[cargo[0]] = cargo[1]
        return ship
