import tdl
#
class Menu:

    def __init__(self, menu_width, menu_height, options = []):
        self.options = options
        self.console = tdl.Console(menu_width, menu_height)
        self.current_option = 0
        self.ACTION_KEYS = {
        'UP' : 'up',
        'DOWN' : 'down',
        'ENTER' : 'select'
        }
        self.NORMAL_COLOR = (255,255,255)
        self.HIGHLIGHT_COLOR= (255,255,0)

    def add_option(self, new_option):
        self.options.append(new_option)

    def detect_events(self):
        delta = 0
        for event in tdl.event.get():
            if event.type == 'KEYDOWN' and event.keychar != 'TEXT':
                action = self.ACTION_KEYS.get(event.keychar, (0,0))
                #(str(action))
                if action == 'up':
                    delta = -1
                elif action == 'down':
                    delta = +1
                #(delta)
                self.current_option += delta
                #(self.current_option)
                if self.current_option < 0:
                    self.current_option = 0
                elif self.current_option > len(self.options)-1:
                    self.current_option = len(self.options)-1
                #(self.current_option)
                return action

    def render_menu(self, sw, sh):
        i = 0
        for option in self.options:
            if i == self.current_option:
                self.console.draw_str(sw//2-len(self.options[self.current_option].display_string)//2, sh*1//4+i,self.options[self.current_option].display_string, bg=None, fg=self.HIGHLIGHT_COLOR)
            else:
                self.console.draw_str(sw//2-len(self.options[i].display_string)//2, sh*1//4+i, self.options[i].display_string, bg=None, fg=self.NORMAL_COLOR)
            i += 1

class Option:

    def __init__(self, name, display_string):
        self.name = name
        self.display_string = display_string
