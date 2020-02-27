import tdl
from .display import GameObject
from .system import System, Planet
from .sector import Sector
import math
from .component import *
from .timer import Timer
from .ui import Panel
#TODO: Move UI stuff to Player
#TODO: Test this file
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
    
    def get_sensors(self):
        results = []
        for component in self.componentlist:
            if type(component) is Sensor:
                for key in component.sensor_types:
                    

