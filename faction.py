from system import *
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

    def to_json(self):
        colonylist = []
        for colony in self.colonies:
            colonylist.append(colony.to_json())
        systemlist = []
        for system in self.claimed_systems:
            systemlist.append(system.name)

        json_data = {
            'name' : self.name,
            'red' : self.red,
            'green' : self.green,
            'blue' : self.blue,
            'colonies' : colonylist,
            'systems' : systemlist
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        name = json_data.get('name')
        red = json_data.get('red')
        green = json_data.get('green')
        blue = json_data.get('blue')
        colonylist = json_data.get('colonies')
        systemlist = json_data.get('systems')

        empire = Empire(name, red, green, blue)
        empire.colonies = colonylist
        empire.claimed_systems = systemlist
        return empire


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

    def to_json(self):
        buildinglist = []
        for building in self.buildings:
            pass #Buildings dont exist yet
            # buildinglist.append(building.to_json())

        json_data = {
            'planet' : self.planet.name,
            'owner' : self.owner.name,
            'population' : self.population,
            'food' : self.food,
            'minerals' : self.minerals,
            'energy' : self.energy,
            'industry' : self.industry,
            'buildinglist' : buildinglist
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        planet = json_data.get('planet')
        owner = json_data.get('owner')
        population = json_data.get('population')
        food = json_data.get('food')
        minerals = json_data.get('minerals')
        energy = json_data.get('energy')
        industry = json_data.get('industry')
        buildinglist = json_data.get('buildinglist')

        colony = Colony(planet, owner, population, food, minerals, energy)
        colony.buildings = buildinglist

        return colony
