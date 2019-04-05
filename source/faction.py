from .system import *

#TODO Figure out how Empires actually work. May require massive overhaul of existing code.
#TODO Test this file

class Empire:
    def __init__(self, name, red, green, blue):
        self.name = name
        self.red = red
        self.green = green
        self.blue = blue
        self.colonies = []
        self.claimed_systems = []

    def add_colony(self, planet, system):
        planet.owner = self
        planet.colony = Colony(planet, self)
        self.colonies.append(planet.colony)
        if system in self.claimed_systems:
            pass
        else:
            self.claimed_systems.append(system)


class Colony:
    def __init__(self, planet, owner, pop=1, food=1, minerals=0, energy=0, industry=0):
        self.planet = planet
        self.owner = owner
        self.population = pop
        self.food = food
        self.minerals = minerals
        self.energy = energy
        self.industry = industry
        self.buildings = []

    def process_turn(self):
        if self.population > self.food:
            self.population = self.food
        if self.industry > min(self.energy, self.minerals):
            self.industry = min(self.energy, self.minerals)
