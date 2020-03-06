from source.component import Reactor, Capacitor, Capacitor, CargoBay, Sensor, Component, Engine
from source.resource import Uranium, Solar

#TODO: Put this in an external file and load these from it

fission_reactor_0 = Reactor("Primitive Fission Reactor", "FISN0", 12, Uranium, 1, 15, 100)
fission_reactor_1 = Reactor("Early Fission Reactor", "FISN1", 10, Uranium, 1, 20, 100)
fission_reactor_2 = Reactor("Fission Reactor", "FISN2", 10, Uranium, 1, 20, 200)
fission_reactor_3 = Reactor("Advanced Fission Reactor", "FISN3", 8, Uranium, 1, 25, 400)

battery_0 = Capacitor("Primitive Battery", "B0", 2, 100)
battery_1 = Capacitor("Battery", "B1", 1, 100)

solar_panel_0 = Reactor("Primitive Solar Panels", "--SP0--", 3, Solar, 0, 6, 0)
solar_panel_1 = Reactor("Early Solar Panels", "--SP1--", 2, Solar, 0, 8, 0)

cargo_bay = CargoBay("CargoBay", "H", 1, 10)

radar_0 = Sensor("Primitive Radar", "RDR0", 5, 2, 5, {'thermal' : 1, 'electromagnetic': 1, 'optical': 2})

armor = Component("Armor", "A", 1)

docking_bay_0 = Component("Primitive Docking Bay", "DOCK0", 100)

#gas_harvester_0 =

basic_engine_0 = Engine("Magnetic Field Drive", "MgD0", 1, 20, 1)
