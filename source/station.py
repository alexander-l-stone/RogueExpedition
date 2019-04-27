from .display import GameObject
from .ship import Ship

class Station(GameObject):
    def __init__(self, char, color, x, y, name, station_type, system=None, faction=None):
        GameObject.__init__(self, char, color, x, y)
        self.name = name
        self.type = station_type
    
    def onCollide(self, other, dx, dy):
        if self.type == 'uranium-debug':
            if other.vector.getMagnitude() < 2:
                return {'result': 'uranium-debug',
                        'target': self,}
            else:
                return {'result': 'move'}