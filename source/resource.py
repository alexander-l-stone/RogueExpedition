#TODO: Add more resources
#TODO: Test this file
class Resource:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def to_json(self):
        json_data = {
            'name' : self.name,
            'symbol' : self.symbol
        }
        return json_data

    def from_json(json_data):

        resource = Resource(json_data['name'], json_data['symbol'])
        return resource

Uranium = Resource("Uranium", "U")
Helium3 = Resource("Helium 3", "He3")
Solar = Resource("Solar", "y" )
