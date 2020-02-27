from .system import *
from .resource import *
#TODO Test the classes in this file
#This is the base class for all ship components. This is for TYPE of component, not individual components
class Component:
    def __init__(self, name, charstring, size, active=True, damaged=False):
        self.name = name
        self.active = active
        self.char = charstring
        self.damaged = damaged
        self.size = size

    def activate(self, ship, ui):
        return ('component', 0)


#Describes Sensors. Currently only stores sensor range. TODO: Add something to allow sensors to interact with ECM and Cloaks.
class Sensor(Component):
    def __init__(self, name, charstring, size, sensor_range, power_cost, sensor_types, active=True, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.sensor_range = sensor_range
        self.power_cost = power_cost
        self.sensor_types = sensor_types

    #Sensors draw in power for their use.
    def activate(self, ship, ui):
        if ship.current_power >= self.power_cost and self.active and not self.damaged:
            return ('sensor', self.power_cost)
        elif ship.current_power >= self.power_cost and not self.active and not self.damaged:
            if not self.active == True:
                ui.message("Turning on " + self.name, 'engineering')
                self.active = True
                return ('sensor', self.power_cost)
        else:
            if not self.active == False:
                ui.message("Turning off " + self.name, 'engineering')
            self.active = False
            return ('sensor', 0)


class CargoBay(Component):
    def __init__(self, name, charstring, size, cargo_amount, active=True, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.cargo_amount = cargo_amount

    def activate(self, ship, ui):
        return ('cargo', 0)


class Capacitor(Component):
    def __init__(self, name, charstring, size, power_amount, active=True, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.power_amount = power_amount


class Reactor(Component):
    def __init__(self, name, charstring, size, fuel_type, fuel_cost, power_produced, max_tank, active=True, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.fuel_type = fuel_type
        self.fuel_cost = fuel_cost
        self.power_produced = power_produced
        self.max_tank = max_tank
        self.current_tank = self.max_tank

    def activate(self, ship, ui):
        return ('reactor', 0)

    def produce_power(self, ui, ship):
        fuel = ship.cargo_list.get(self.fuel_type)
        if self.active and not self.damaged:
            if self.max_tank == 0 and self.fuel_cost == 0:
                return self.power_produced
            elif self.max_tank == 0:
                if ship.cargo_list[fuel] < self.fuel_cost:
                    ui.message("We do not have enough " + self.fuel_type.name + " for our " + self.name, 'engineering')
                    self.active = False
                    return 0
                else:
                    ship.cargo_list[fuel] -= self.fuel_cost
                    return self.power_produced
            else:
                if self.current_tank - self.fuel_cost < 0:
                    if ship.cargo_list[fuel] < self.fuel_cost:
                        ui.message("We do not have enough " + self.fuel_type.name + " for our " + self.name, 'engineering')
                        self.active = False
                        return 0
                    else:
                        ship.cargo_list[fuel] -= self.fuel_cost
                        self.current_tank = self.max_tank - self.fuel_cost
                        return self.power_produced
                else:
                    self.current_tank = self.max_tank - self.fuel_cost
                    return self.power_produced
        else:
            return 0


#Resources Harvested is a Dictionary, with the Key being the Resource, and the value being the amount of that Resource that is harvested
class ResourceHarvester(Component):
    def __init__(self, name, charstring, size, resources_harvested, power_cost, active=False, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.resources_harvested = resources_harvested
        self.power_cost = power_cost

    def activate(self, ship, ui):
        if self.active:
            return ('harvester', self.power_cost)
        else:
            return ('harvester', 0)

    def harvest(self, ui, ship):
        if not isinstance(ship.location, Planet):
            return False
        else:
            if ship.current_power < self.power_cost:
                ui.message("We do not have enough power to run the " + self.name, 'engineering')
                return False
            else:
                if (ship.x > -1 and ship.x < 1) and (ship.y > -1 and ship.y < 1):
                    if ship.location.planet_type == 'Gas Giant' or ship.location.planet_type == 'Liquid Giant':
                        if Helium3 in self.resources_harvested:
                            ui.message("Harvesting Helium 3 from " + ship.location.name, 'engineering')
                            ship.current_power -= self.power_cost
                            return True
                    elif ship.location.planet_type == 'Barren' or ship.location.planet_type == 'Terran' or ship.location.planet_type == 'Super Terran':
                        if Uranium in self.resources_harvested:
                            ui.message("Harvesting Uranium from " + ship.location.name, 'engineering')
                            ship.current_power -= self.power_cost
                            return True
                else:
                    ui.message("Move closer to the planet to harvest", 'engineering')
                    return False


class Engine(Component):
    def __init__(self, name, charstring, size, thrust, power_cost, active=True, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.thrust = thrust
        self.power_cost = power_cost

    def activate(self, power, ui):
        return ('engine', self.power_cost)

    def check_thrust(self, ui, ship):
        if ship.current_power >= self.power_cost and self.active and not self.damaged:
            return self.thrust
        else:
            ui.message("We do not have enough power to run our " + self.name, 'engineering')
            self.active = False
            return 0
