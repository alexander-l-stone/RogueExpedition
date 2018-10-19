#This is the basic object for moving and drawing game objects
#TODO Test the classes in this file;
class GameObject:
    def __init__(self, char, color, x, y):
        self.char = char
        self.color = color
        self.x = x
        self.y = y

    def draw(self, console, topx, topy, sw, sh):
        if (self.x-topx > 0) and (self.y-topy > 0) and (self.x-topx < sw) and (self.y-topy < sh):
            console.draw_char(self.x-topx, self.y-topy, self.char, self.color, bg=None)

    def clear(self, console, topx, topy, sw, sh, clearbg=None):
        if (self.x-topx > 0) and (self.y-topy > 0) and (self.x-topx < sw) and (self.y-topy < sh):
            console.draw_char(self.x-topx, self.y-topy, ' ', bg=clearbg)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def to_json(self):
        char = self.char
        color = self.color
        x = self.x
        y = self.y

        json_data = {
            'char' : char,
            'color' : color,
            'x' : x,
            'y' : y
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        x = json_data.get('x')
        y = json_data.get('y')
        char = json_data.get('char')
        color = json_data.get('color')

        entity = GameObject(char, color, x, y)
        return entity
