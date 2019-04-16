from .display import GameObject
from .system import System, Planet
from .sector import Sector
import math

class NewtonObject(GameObject):
    def __init__(self, char, color, x, y, vector=Vector(0,0)):
        GameObject.__init__(self, char, color, x, y)
        self.vector = vector
    
    def move(self, location):
        new_x = self.x + self.vector.dx
        new_y = self.y + self.vector.dy
        result = None
        for obj in location.objlist:
            if (new_x == obj.x) and (new_y == obj.y):
                result = obj.onCollide(self)
                break
        if isinstance(location, Sector) and result == None:
            for system in location.systemlist:
                if (new_x == system.x) and (new_y == system.y):
                    result = system.onCollide(self)
                    break
        elif isinstance(location, System) and result == None:
            for planet in location.planetlist:
                if (new_x == planet.x) and (new_y == system.y):
                    result = system.onCollide(self)
                    break
        elif isinstance(location, Planet) and result == None:
            for moon in location.moonlist:
                if (new_x == moon.x) and (new_y == moon.y):
                    result = system.onCollide(self)
                    break
        if result == None:
            result = {'result': 'move'}
        return result

    def getGhostPosition(self):
        return (self.x+self.vector.dx, self.y+self.vector.dy)


class Vector:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
    
    def addVector(self, vector):
        self.dx = self.dx + vector.dx
        self.dy = self.dy + vector.dy
    
    def addPolar(self, radius, theta):
        self.dx = int(float(self.dx) + radius*math.cos(theta))
        self.dy = int(float(self.dy) + radius*math.sin(theta))

    def getMagnitude(self):
        return math.sqrt(self.dx*self.dx + self.dy*self.dy)