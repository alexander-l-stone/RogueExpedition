from .display import GameObject
from .ship import Ship

class Station(GameObject):
    def __init__(self, char, color, x, y, name, station_type, system=None, faction=None):
        GameObject.__init__(self, char, color, x, y)
        self.name = name
        self.type = station_type
        self.sensor_information = {}
    
    def onCollide(self, other, dx, dy):
        if self.type == 'uranium-debug':
            if isinstance(other, Ship):
                key = other.cargo_list.get('Uranium')
                if key == None:
                    other.cargo_list['Uranium'] = 30
                else:
                    other.cargo_list['Uranium'] = 30
                    if other.player:
                        other.ui.message('We refueled upto 30 Uranium at ' + self.name, 'engineering')
        return False