from system import *
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

    def to_json(self):
        name = self.name
        active = self.active
        char = self.char
        size = self.size

        json_data = {
            'name' : name,
            'active' : active,
            'charstring' : char,
            'damaged' : damaged,
            'size' : size
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        active = json_data.get('active')
        charstring = json_data.get('charstring')
        damaged = json_data.get('damaged')
        size = json_data.get('size')

        component = Component(name, charstring, size, active=active, damaged=damaged)
        return component
#Describes Sensors. Currently only stores sensor range. TODO: Add something to allow sensors to interact with ECM and Cloaks.
class Sensor(Component):
    def __init__(self, name, charstring, size, sensor_range, power_cost, active=True, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.sensor_range = sensor_range
        self.power_cost = power_cost

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

    def to_json(self):
        name = self.name
        active = self.active
        char = self.char
        damaged = self.damaged
        size = self.size
        sensor_range = self.sensor_range
        power_cost = self.power_cost

        json_data = {
            'name' : self.name,
            'active' : self.active,
            'charstring' : self.char,
            'damaged' : self.damaged,
            'size' : self.size,
            'sensor_range' : self.sensor_range,
            'power_cost' : self.power_cost
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        active = json_data.get('active')
        charstring = json_data.get('charstring')
        damaged = json_data.get('damaged')
        size = json_data.get('size')
        sensor_range = json_data.get('sensor_range')
        power_cost = json_data.get('power_cost')

        component = Component(name, charstring, size, sensor_range, power_cost, active=active, damaged=damaged)
        return component

class CargoBay(Component):
    def __init__(self, name, charstring, size, cargo_amount, active=True, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.cargo_amount = cargo_amount

    def activate(self, ship, ui):
        return ('cargo', 0)

    def to_json(self):
        name = self.name
        active = self.active
        charstring = self.char
        damaged = self.damaged
        size = self.size
        cargo_amount = self.cargo_amount

        json_data = {
            'name' : name,
            'active' : active,
            'charstring' : char,
            'damaged' : damaged,
            'size' : size,
            'cargo_amount' : cargo_amount
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        active = json_data.get('active')
        charstring = json_data.get('charstring')
        damaged = json_data.get('damaged')
        size = json_data.get('size')
        cargo_amount = json_data.get('cargo_amount')

        component = Component(name, charstring, size, cargo_amount, active=active, damaged=damaged)
        return component

class Capacitor(Component):
    def __init__(self, name, charstring, size, power_amount, active=True, damaged=False):
        Component.__init__(self, name, charstring, size, active, damaged)
        self.power_amount = power_amount

    def active(self, ship, ui):
        return ('capacitor', 0)

    def to_json(self):
        name = self.name
        active = self.active
        char = self.char
        damaged = self.damaged
        size = self.size
        power_amount = self.power_amount

        json_data = {
            'name' : name,
            'active' : active,
            'charstring' : char,
            'damaged' : damaged,
            'size' : size,
            'power_amount' : power_amount
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        active = json_data.get('active')
        charstring = json_data.get('charstring')
        damaged = json_data.get('damaged')
        size = json_data.get('size')
        power_amount = json_data.get('power_amount')

        component = Component(name, charstring, size, power_amount, active=active, damaged=damaged)
        return component

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

    def to_json(self):
        name = self.name
        active = self.active
        char = self.char
        damaged = self.damaged
        size = self.size
        fuel_type = self.fuel_type.to_json()
        fuel_cost = self.fuel_cost
        power_produced = self.power_produced
        max_tank = self.max_tank
        current_tank = self.current_tank

        json_data = {
            'name' : name,
            'active' : active,
            'charstring' : char,
            'damaged' : damaged,
            'size' : size,
            'fuel_type' : fuel_type,
            'fuel_cost' : fuel_cost,
            'power_produced' : power_produced,
            'max_tank' : max_tank,
            'current_tank' : current_tank
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        active = json_data.get('active')
        charstring = json_data.get('charstring')
        damaged = json_data.get('damaged')
        size = json_data.get('size')
        fuel_type = json_data.get('fuel_type')
        fuel_cost = json_data.get('fuel_cost')
        power_produced = json_data.get('power_produced')
        max_tank = json_data.get('max_tank')
        current_tank = json_data.get('current_tank')

        component = Component(name, charstring, size, fuel_type, fuel_cost, power_produced, max_tank, active=active, damaged=damaged)
        component.current_tank = current_tank
        return component

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

    def to_json(self):
        json_data = {
            'name' : self.name,
            'active' : self.active,
            'charstring' : self.char,
            'damaged' : self.damaged,
            'size' : self.size,
            'resources_harvested' : self.resources_harvested.to_json(),
            'power_cost' : self.power_cost
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        active = json_data.get('active')
        charstring = json_data.get('charstring')
        damaged = json_data.get('damaged')
        size = json_data.get('size')

        component = Component(name, charstring, size, active=active, damaged=damaged)
        return component

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

    def to_json(self):
        json_data = {
            'name' : self.name,
            'active' : self.active,
            'charstring' : self.char,
            'damaged' : self.damaged,
            'size' : self.size,
            'thrust' : self.thrust,
            'power_cost' : self.power_cost
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        active_state = json_data.get('active')
        charstring = json_data.get('charstring')
        damage_state = json_data.get('damaged')
        size = json_data.get('size')
        thrust = json_data.get('thrust')
        power_cost = json_data.get('power_cost')

        engine = Engine(name, charstring, size, thrust, power_cost, active=active_state, damaged=damage_state)
        return engine
