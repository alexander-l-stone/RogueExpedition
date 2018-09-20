import tdl
from display import GameObject
from system import System, Planet
from sector import Sector
import math
from component import *
from timer import Timer
#TODO: Move UI stuff to Player
class Ship(GameObject):

    def __init__(self, char, color, x, y, name, model, size, timer, ui=None, componentlist=None, system=None, isPlayer=False, faction=None):
        GameObject.__init__(self, char, color, x, y)
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

    def get_thrust(self):
        thrust = 0
        size = 0
        for component in self.componentlist:
            size += component.size
            if isinstance(component, Engine):
                thrust += component.check_thrust(self.ui, self)
        return thrust/size

    def to_json(self):
        name = self.name
        x = self.x
        y = self.y
        char = self.char
        color = self.color
        model = self.model
        cargolist = []
        for key,val in self.cargo_list.items():
            with open('json.log', 'a') as f:
                f.write("---\n")
                f.write("Resource: " + key + " \n")
            new_cargo = key.to_json()
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

        newComponentList = []
        for component in componentlist:
            newComponent = Ship.component_from_json(component)
            newComponentList.append(newComponent)

        ship = Ship(char, color, x, y, name, model, size, Timer.from_json(clock), ui=None, componentlist=newComponentList, isPlayer=player, faction=faction)
        ship.location = location
        ship.alert = alert
        for cargo in cargolist:
            ship.cargolist[cargo[0]] = cargo[1]
        return ship

    @staticmethod
    def component_from_json(json_data):
        with open('test.log', 'a') as f:
            f.write('\n')
            f.write(str(json_data) + '\n')
            f.closed
        return {
            'component' : Component.from_json(json_data),
            'sensor' : Sensor.from_json(json_data),
            'cargo' : CargoBay.from_json(json_data),
            'capacitor' : Capacitor.from_json(json_data),
            'reactor' : Reactor.from_json(json_data),
            'harvester' : ResourceHarvester.from_json(json_data),
            'engine' : Engine.from_json(json_data)
        }.get(json_data['type'])
