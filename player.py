#TODO: Other than just holding a ship, figure out what other things a Player object needs to hold
class Player:
    def __init__(self, ship):
        #TODO: Move the UI parts of Ship here.
        self.ship = ship

    def to_json(self):
        json_data = {
            'ship' : self.ship.to_json()
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        return Player(json_data['ship'])
