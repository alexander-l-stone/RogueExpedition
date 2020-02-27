import tdl
import textwrap
from .system import *

#TODO: Test this file
class Panel:
    def __init__(self, screen_width, panel_height, msg_height, msg_width, msg_x):
        self.panel = tdl.Console(screen_width, panel_height)
        self.screen_width = screen_width
        self.panel_height = panel_height
        self.msg_height = msg_height
        self.msg_width = msg_width
        self.msg_x = msg_x
        self.msgs = []

    def render_border(self):
        self.panel.draw_rect(0,0, self.screen_width, 1, None, bg=(200,200,200))
        self.panel.draw_rect(0,1, self.screen_width, self.panel_height, None, bg=(20,20,20))

    def render_bar(self, x, y, total_width, name, value, maximum, bar_color, back_color):
        bar_width = int(float(value) / maximum* total_width)
        self.panel.draw_rect(x, y, total_width, 1, None, bg=back_color)
        if bar_width > 0:
            self.panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)
        text = name + ' ' + str(value) + '/' + str(maximum)
        x_centered = x + (total_width-len(text))//2
        self.panel.draw_str(x_centered, y, text, fg=(0,0,0), bg=None)

    def render_coordinates(self, center, y, ship):
        message = str(ship.location.name) + ": " + str(ship.x) + ", " + str(-ship.y)
        self.panel.draw_str(center-len(message)//2, y, message, bg=None)
        if isinstance(ship.location, System):
            type_message = str(ship.location.star.stellar_type) + ", Mass: " + str(ship.location.star.mass)
            self.panel.draw_str(center-len(type_message)//2, y+1, type_message, bg=None)
        elif isinstance(ship.location, Planet):
            type_message = str(ship.location.planet_type)
            self.panel.draw_str(center-len(type_message)//2, y+1, type_message, bg=None)
    
    def render_sensors(self, center, y, ship):
        category_name = "Sensors:"
        messages = ship.get_sensors()


    def clear(self):
        self.panel.clear(fg=(255,255,255), bg=(0,0,0))

    def message(self, new_msg, msg_type, color = (255,255,255)):
        new_msg_lines = textwrap.wrap(str(new_msg), self.msg_width)
        for msg in new_msg_lines:
            print(msg)
        if msg_type == 'helm':
            for line in new_msg_lines:
                if len(self.msgs) >= self.msg_height*2:
                    del self.msgs[0]
                self.msgs.append((line, (75,255,75)))
        elif msg_type == 'engineering':
            for line in new_msg_lines:
                if len(self.msgs) >= self.msg_height*2:
                    del self.msgs[0]
                self.msgs.append((line, (255,115,60)))
        elif msg_type == 'tactical':
            for line in new_msg_lines:
                if len(self.msgs) >= self.msg_height*2:
                    del self.msgs[0]
                self.msgs.append((line, (255,0,0)))
        elif msg_type == 'comms':
            for line in new_msg_lines:
                if len(self.msgs) >= self.msg_height*2:
                    del self.msgs[0]
                self.msgs.append((line, (255,66,255)))
        elif msg_type == 'science':
            for line in new_msg_lines:
                if len(self.msgs) >= self.msg_height*2:
                    del self.msgs[0]
                self.msgs.append((line, (0,100,255)))
        elif msg_type == 'debug':
            for line in new_msg_lines:
                if len(self.msgs) >= self.msg_height*2:
                    del self.msgs[0]
                self.msgs.append((line, (255,255,255)))

    def render_messages(self):
        y = 3
        self.panel.draw_str(self.msg_x, y, "Messages: ", bg=None, fg=(255,255,255))
        self.panel.draw_str(self.screen_width - self.msg_width - self.msg_x, y, "Messages: ", bg=None, fg=(255,255,255))
        y += 1
        num_messages = 0
        for (line, color) in self.msgs:
            #if (line == "anomaly."):
            #    for msg in self.msgs:
            #        print(msg)
            if num_messages < self.msg_height:
                self.panel.draw_str(self.msg_x, y, line, bg=None, fg=color)
            if num_messages >= self.msg_height:
                self.panel.draw_str(self.screen_width - self.msg_width - self.msg_x, y-self.msg_height, line, bg=None, fg=color)
            y+=1
            num_messages+=1
