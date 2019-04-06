import tdl
from source.system import *
from source.ship import *
from source.display import *
from source.sector import Sector
from source.ui import *
from data.base.component_list import *
import copy
from source.galaxy import *
from source.constants import *
from source.player import Player
from source.timer import Timer
from source.menu import *
from source.faction import *
import math
from source.action_manager import *
import pickle
from source.station import Station

#TODO: Clean up this file and remove constants/import them from files

class Game:
    def __init__(self):
        self.SCREEN_WIDTH = 110
        self.SCREEN_HEIGHT = 60
        self.LIMIT_FPS = 20
        tdl.set_font('arial12x12.png', greyscale = True, altLayout = True)
        self.FOV_ALGO = 'Basic'
        self.PANEL_HEIGHT = 12
        self.BAR_WIDTH = 20
        self.PANEL_Y = self.SCREEN_HEIGHT-self.PANEL_HEIGHT
        self.MSG_X = 2
        self.MSG_WIDTH = 30
        self.MSG_HEIGHT = self.PANEL_HEIGHT - 5
        self.SECTOR_HEIGHT = 250
        self.SECTOR_WIDTH = 250
        self.clock = Timer(minutes=732312120)

        self.MOVEMENT_KEYS = {
            'UP': [0,-1],
            'DOWN':[0,1],
            'LEFT':[-1,0],
            'RIGHT':[1,0],
            'KP1':[-1, 1],
            'KP2':[ 0, 1],
            'KP3':[ 1, 1],
            'KP4':[-1, 0],
            'KP6':[ 1, 0],
            'KP7':[-1,-1],
            'KP8':[ 0,-1],
            'KP9':[ 1,-1]
            }
        self.ACTION_KEYS = {
            'J' : 'jump',
            'j' : 'jump',
            'D' : 'debug',
            'd' : 'debug',
            'M' : 'menu',
            'm' : 'menu',
            'w' : 'where',
            'W' : 'where'
            }
        #Y is down, X is Right
        self.CENTERX = self.SCREEN_WIDTH//2
        self.CENTERY = self.SCREEN_HEIGHT//2
        self.system_names = {}
        self.milky_way = Galaxy()
        self.console = tdl.Console(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.ui = Panel(self.SCREEN_WIDTH, self.PANEL_HEIGHT, self.MSG_HEIGHT, self.MSG_WIDTH, self.MSG_X)
        self.current_menu = None
        self.options_menu = Menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.main_menu = Menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        #FIXME: The menu's are both broken in the same way. Each menu has the others menu's options in it. No idea what is causing it
        exit = Option('exit', "Exit")
        new_game = Option('new', "New Game")
        load_game = Option('load', "Load Game")
        save_game = Option('save', "Save Game")
        options = Option('blank', "Options")
        self.main_menu.add_option(new_game)
        self.main_menu.add_option(load_game)
        self.main_menu.add_option(exit)
        self.options_menu.add_option(save_game)
        self.options_menu.add_option(options)
        self.options_menu.add_option(exit)
        # with open('menu.log', 'a') as f:
        #     f.write("---\n")
        #     f.write("Main Menu Contents: \n")
        #     for option in self.main_menu.options:
        #         f.write(option.name + "\n")
        #     f.write("Options Menu Contents: \n")
        #     for option in self.options_menu.options:
        #         f.write(option.name + "\n")
        #     f.write(str(self.main_menu == self.options_menu))
        #     f.closed
        self.main_window = tdl.init(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, title="Space", fullscreen = False)
        self.fov_recompute = True
        self.game_state = 'playing'

    def generate_galaxy(self):

        #TODO: Load the initial system from a file instead of hard code
        Terra_Prime = System('Terra Prime', randrange(0,251), randrange(0,251), False)
        Terra_Prime_Star = Star('O', (255,255,50), 0, 0, 'Terra Prime', 'Yellow', 4)
        Terra_Prime.star = Terra_Prime_Star
        New_Terra = Planet('o', (10, 50, 255), 7, 5, 5, 'Terran', 'New Terra')
        Chandra = Planet('o', (38,43,41), 2, -2, -1, 'Barren', 'Chandra')
        New_Terra.moonlist.append(Chandra)
        New_Terra.system = Terra_Prime
        New_Terra.planet_limit = Ring('#', (255,255,255), 10, 'Planet Limit', 'New Terra Limit')
        Terra_Prime.planetlist.append(New_Terra)
        Ares = Planet('o', (160, 80, 40), 9, -6, 6, 'Barren', 'Ares')
        Ares.planet_limit = Ring('#', (255,255,255), 4, 'Planet Limit', 'Ares Limit')
        Terra_Prime.planetlist.append(Ares)
        Ares.system = Terra_Prime
        Zeus = Planet('o', (90, 80, 80), 11, -8, 7, 'Barren', 'Zeus')
        Zeus.planet_limit = Ring('#', (255,255,255), 7, 'Planet Limit', 'Zeus Limit')
        Terra_Prime.planetlist.append(Zeus)
        Zeus.system = Terra_Prime
        Hera = Planet('o', (110, 70, 85), 15, 15, 4, 'Barren', 'Hera')
        Enyo = Planet('o', (140, 70, 20), 5, 3, -4, 'Barren', 'Enyo')
        Hera.moonlist.append(Enyo)
        Hera.system = Terra_Prime
        Hera.planet_limit = Ring('#', (255,255,255), 8, 'Planet Limit', 'Hera Limit')
        Terra_Prime.planetlist.append(Hera)
        Odin = Planet('0', (255, 170, 0), 23, -22, -5, 'Gas Giant', 'Odin')
        Huginn = Planet('o', (70, 25, 0), 5, 4, 3, 'Barren', 'Huginn')
        Muninn = Planet('o', (60, 60, 60), 10, -3, 10, 'Barren', 'Muninn')
        Odin.moonlist.append(Huginn)
        Odin.moonlist.append(Muninn)
        Odin.planet_limit = Ring('#', (255,255,255), 15, 'Planet Limit', 'Odin Limit')
        Terra_Prime.planetlist.append(Odin)
        Odin.system = Terra_Prime
        Terra_Prime_Belt = Ring('*', (70,45,15),39, 'Asteroid Belt', 'The Graveyard')
        Terra_Prime.planetlist.append(Terra_Prime_Belt)
        Kronos = Planet('0', (180,0,200), 71, 6, 71, 'Gas Giant', 'Kronos')
        Kronos_Belt = Ring('*', (140,255,255), 2, 'Ice Belt', 'The Belt')
        Rhea = Planet('o', (50, 30, 10), 6, -5, 4, 'Barren', 'Rhea')
        Tartarus = Planet('o', (42, 42, 42), 9, -8, 4, 'Barren', 'Tartarus')
        Kronos.moonlist.append(Kronos_Belt)
        Kronos.moonlist.append(Rhea)
        Kronos.moonlist.append(Tartarus)
        Kronos.planet_limit = Ring('#', (255,255,255), 12, 'Planet Limit', 'Kronos Limit')
        Terra_Prime.planetlist.append(Kronos)
        Kronos.system = Terra_Prime
        Varuna = Planet('0', (0,130,180), 135, -57, -122, 'Liquid Giant', 'Varuna')
        Ganges = Planet('o', (75, 125, 255), 2, -2, -1, 'Frozen', 'Ganges')
        Yami = Planet('o', (60, 110, 255), 6, 5, 3, 'Frozen', 'Yami')
        Varuna.moonlist.append(Ganges)
        Varuna.moonlist.append(Yami)
        Varuna.planet_limit = Ring('#', (255,255,255), 15, 'Planet Limit', 'Varuna Limit')
        Terra_Prime.planetlist.append(Varuna)
        Varuna.system = Terra_Prime
        Ymir = Planet('0', (0, 255, 255), 263, -123, 232, 'Liquid Giant', 'Ymir')
        The_Wall = Ring('*', (140,255,255), 3, 'Ice Belt', 'The Wall')
        Ymir.moonlist.append(The_Wall)
        Terra_Prime.planetlist.append(Ymir)
        Ymir.system = Terra_Prime
        Terra_Prime.hyperlimit = Ring('#', (255,100,100), 294, 'Hyperlimit', 'Terra Prime Hyperlimit')
        #Test_Wormhole = Wormhole('X', (200,66, 244), 250, Terra_Prime)
        #Test_Wormhole.x = 191
        #Test_Wormhole.y = 161

        Terran_Coalition = Empire('Terran Coalition', 0, 0, 100)
        Terran_Coalition.add_colony(New_Terra, Terra_Prime)
        Terran_Coalition.colonies[0].population = 15
        Terran_Coalition.colonies[0].food = 15
        Terran_Coalition.colonies[0].minerals = 5
        Terran_Coalition.colonies[0].energy = 5
        Terran_Coalition.colonies[0].industry = 5
        start_system = Terra_Prime
        start_system.explored = True
        terran_sector = Sector('Terran Sector', 'normal', 0, 0, self.SECTOR_WIDTH, self.SECTOR_HEIGHT, sysnames=self.system_names)
        terran_sector.systemlist.append(start_system)
        start_system.sector = terran_sector
        debug_station = Station('S', (Terran_Coalition.red, Terran_Coalition.green, Terran_Coalition.blue), 1, 1, 'Prime Station', 'uranium-debug', system=New_Terra)
        New_Terra.objlist.append(debug_station)
        self.system_names[terran_sector.name] = 1
        terran_sector.generate()
        self.milky_way.add_sector(terran_sector)
        self.start_system = Terra_Prime
        self.start_planet = New_Terra
        self.milky_way.factions.append(Terran_Coalition)

    def generate_player_ship(self):
        #TODO: Load the initial ship from a file instead of hard code
        self.player_ship = Ship('e', (0,0,255), -1, -1, 'Korolev', 'Magellan', 30, self.clock, ui=self.ui, isPlayer=True)
        self.player_ship.location = self.start_planet
        self.start_planet.objlist.append(self.player_ship)
        magellan_solar_1 = copy.copy(solar_panel_0)
        magellan_solar_2 = copy.copy(solar_panel_0)
        magellan_reactor_1 = copy.copy(fission_reactor_1)
        magellan_battery_1 = copy.copy(battery_1)
        magellan_battery_2 = copy.copy(battery_1)
        magellan_battery_3 = copy.copy(battery_1)
        magellan_battery_4 = copy.copy(battery_1)
        magellan_battery_5 = copy.copy(battery_1)
        magellan_battery_6 = copy.copy(battery_1)
        magellan_battery_7 = copy.copy(battery_1)
        magellan_battery_8 = copy.copy(battery_1)
        magellan_battery_9 = copy.copy(battery_1)
        magellan_battery_10 = copy.copy(battery_1)
        magellan_sensor_1 = copy.copy(radar_0)
        magellan_drive_1 = copy.copy(basic_engine_0)
        magellan_drive_2 = copy.copy(basic_engine_0)
        self.player_ship.componentlist.append(magellan_solar_1)
        self.player_ship.componentlist.append(magellan_solar_2)
        self.player_ship.componentlist.append(magellan_reactor_1)
        self.player_ship.componentlist.append(magellan_battery_1)
        self.player_ship.componentlist.append(magellan_battery_2)
        self.player_ship.componentlist.append(magellan_battery_3)
        self.player_ship.componentlist.append(magellan_battery_4)
        self.player_ship.componentlist.append(magellan_battery_5)
        self.player_ship.componentlist.append(magellan_battery_6)
        self.player_ship.componentlist.append(magellan_battery_7)
        self.player_ship.componentlist.append(magellan_battery_8)
        self.player_ship.componentlist.append(magellan_battery_9)
        self.player_ship.componentlist.append(magellan_battery_10)
        self.player_ship.componentlist.append(magellan_sensor_1)
        self.player_ship.componentlist.append(magellan_drive_1)
        self.player_ship.componentlist.append(magellan_drive_2)
        self.player_ship.calculate_statistics()
        self.player_ship.current_power = self.player_ship.power_max
        #player faction is always the first entery in the galaxy factions menu. FIND BETTER METHOD(player_faction stored in galaxy seperately?)
        self.player_ship.faction = self.milky_way.factions[0]
        self.ui.message("This is Helm, ready to go", 'helm')
        self.ui.message("This is Engineering, ready to go", 'engineering')
        self.ui.message("This is Tactical, ready to go", 'tactical')
        self.ui.message("This is Communications, ready to go", 'comms')
        self.ui.message("This is Science, ready to go", 'science')
        self.player = Player(self.player_ship)
        self.time_since_last_update = 0
        self.total_time_elapsed = 0

    def render_game(self):
        if isinstance(self.player.ship.location, System):
            for drawx in range(0, self.SCREEN_WIDTH):
                for drawy in range (0, self.SCREEN_HEIGHT):
                    rangetoship = math.pow(math.pow(drawx-self.CENTERX,2)+math.pow(drawy-self.CENTERY,2),1/2)
                    if rangetoship <= self.player.ship.sensor_range*5:
                        self.console.draw_char(drawx, drawy, ' ', bg=(15, 15, 15))
            self.player.ship.location.draw(self.console, self.player.ship.x-self.CENTERX, self.player.ship.y-self.CENTERY, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        if isinstance(self.player.ship.location, Sector):
            for drawx in range(0, self.SCREEN_WIDTH):
                for drawy in range (0, self.SCREEN_HEIGHT):
                    rangetoship = math.pow(math.pow(drawx-self.CENTERX,2)+math.pow(drawy-self.CENTERY,2),1/2)
                    if rangetoship <= self.player.ship.sensor_range:
                        self.console.draw_char(drawx, drawy, ' ', bg=(120, 0, 0))
                    else:
                        self.console.draw_char(drawx, drawy, ' ', bg=(60, 0, 0))
            self.milky_way.sector_draw(self.player.ship.location, self.console, self.player.ship.x-self.CENTERX, self.player.ship.y-self.CENTERY, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        if isinstance(self.player.ship.location, Planet):
            self.player.ship.location.planet_draw(self.console, self.player.ship.x - self.CENTERX, self.player.ship.y - self.CENTERY, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.player.ship.draw(self.console, self.player.ship.x-self.CENTERX, self.player.ship.y-self.CENTERY, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.render_clock()
        self.main_window.blit(self.console, 0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 0, 0)
        self.ui.clear()
        self.ui.render_border()
        self.ui.render_bar(self.SCREEN_WIDTH//2-self.BAR_WIDTH//2, 2, self.BAR_WIDTH, 'Energy', self.player.ship.current_power, self.player.ship.power_max, (255,255,0), (255,255,100))
        self.ui.render_coordinates(self.SCREEN_WIDTH//2, 7, self.player.ship)
        self.ui.render_messages()
        self.main_window.blit(self.ui.panel,0, self.PANEL_Y, self.SCREEN_WIDTH, self.PANEL_HEIGHT, 0, 0)
        tdl.flush()
        if isinstance(self.player.ship.location, System):
            self.player.ship.location.clear(self.console, self.player.ship.x-self.CENTERX, self.player.ship.y-self.CENTERY, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        elif isinstance(self.player.ship.location, Sector):
            self.milky_way.sector_clear(self.player.ship.location, self.console, self.player.ship.x-self.CENTERX, self.player.ship.y-self.CENTERY, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        elif isinstance(self.player.ship.location, Planet):
            for drawx in range(0, self.SCREEN_WIDTH):
                for drawy in range(0, self.SCREEN_HEIGHT):
                    self.console.draw_char(drawx, drawy, ' ', bg=(0, 0, 0))
            self.player.ship.location.planet_clear(self.console, self.player.ship.x - self.CENTERX, self.player.ship.y-self.CENTERY, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def render_clock(self):
        self.console.draw_rect(0, 0, self.SCREEN_WIDTH, 0, None, bg=(100,100,100))
        self.console.draw_str(self.SCREEN_WIDTH-40, 0, self.clock.get_text(), (255,255,255))

    def find_time(self, thrust, distance, timefactor):
        return thrust/distance*timefactor

    def main_loop(self):
        while not tdl.event.is_window_closed():
            if self.game_state == 'playing':
                self.render_game()
                for event in tdl.event.get():
                    if event.type == 'KEYDOWN' and event.keychar != 'TEXT' and self.game_state == 'playing':
                        key_x, key_y = self.MOVEMENT_KEYS.get(event.keychar, (0,0))
                        action = self.ACTION_KEYS.get(event.keychar, (0,0))
                        if self.player.ship.get_thrust() <= 0:
                            self.ui.message("We have no working engines.", 'engineering')
                        else:
                            if attemptMove(self.player.ship, self.milky_way, key_x, key_y):
                                x = False
                                y = False
                                time = 0
                                if key_x == 1 or key_x == -1:
                                    x = True
                                if key_y == 1 or key_y == -1:
                                    y = True
                                if isinstance(self.player.ship.location, Sector):
                                    if x and y:
                                        time = int(self.find_time(self.player.ship.get_thrust(), math.sqrt(2), 1440))
                                    else:
                                        time = int(self.find_time(self.player.ship.get_thrust(), 1, 1440))
                                else:
                                    if x and y:
                                        time = int(self.find_time(self.player.ship.get_thrust(), math.sqrt(2), 60))
                                    else:
                                        time = int(self.find_time(self.player.ship.get_thrust(), 1, 60))
                                self.clock.minutes += time
                                self.time_since_last_update += time
                                self.total_time_elapsed += time
                                if isinstance(self.player.ship.location, System):
                                    while self.time_since_last_update >= 60:
                                        self.player.ship.activate(self.ui)
                                        self.time_since_last_update -= 60
                                if isinstance(self.player.ship.location, Planet):
                                    while self.time_since_last_update >= 60:
                                        self.player.ship.activate(self.ui)
                                        self.time_since_last_update -= 60
                                elif isinstance(self.player.ship.location, Sector):
                                    while self.time_since_last_update >= 1440:
                                        self.player.ship.activate(self.ui)
                                        self.time_since_last_update -= 1440
                                self.player.ship.current_clock.minutes = self.clock.minutes
                            else:
                                pass
                        if isinstance(self.player.ship.location, System):
                            for drawx in range(0, self.SCREEN_WIDTH):
                                for drawy in range(0, self.SCREEN_HEIGHT):
                                    self.console.draw_char(drawx, drawy, ' ', bg=(0,0,0))
                        if action == 'jump':
                            attemptJump(self.player.ship, self.clock)
                        if action == 'debug':
                            with open('debug.txt', 'a') as f:
                                f.write(self.player.ship.location)
                                if isinstance(self.player.ship.location, System):
                                    f.write("---\n")
                                    f.write(self.player.ship.location.name + ": \n")
                                    for obj in self.player.ship.location.planetlist:
                                        if isinstance(obj, Planet):
                                            f.write(obj.name + ", radius: " + str(obj.radius) + ", at " + str(obj.x) + ", " + str(obj.y) +"\n")
                                        elif isinstance(obj, Ring):
                                            f.write(obj.name + ", radius: " + str(obj.radius)+ "\n")
                                    f.write("Hyperlimit at " + str(self.player.ship.location.hyperlimit.radius) + "\n")
                                f.closed
                        if action == 'menu':
                            self.game_state = 'menu'
                            self.current_menu = self.options_menu
                            with open('menu.log', 'a') as f:
                                f.write("---\n")
                                f.write("Game Menu Contents: \n")
                                for option in self.current_menu.options:
                                    f.write(option.name + "\n")
                            #(str(self.game_state))
                            self.fov_recompute = True
                        if action == 'where':
                            self.ui.message(str(self.player.ship.location), 'comms')
                        if event.type == 'QUIT':
                            raise SystemExit('Window closed.')
            elif self.game_state == 'menu':
                if self.current_menu == None:
                    self.render_game()
                    self.game_state = 'playing'
                else:
                    self.current_menu.render_menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                    self.main_window.blit(self.current_menu.console, 0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, 0, 0)
                    tdl.flush()
                    action = self.current_menu.detect_events()
                    if action == 'move':
                        pass
                    elif action == 'select':
                        #("I got to the select action")
                        option = self.current_menu.options[self.current_menu.current_option]
                        #(option.name)
                        if option.name == 'blank':
                            pass
                        elif option.name == 'save':
                            self.save_game()
                            self.current_menu.current_option = 0
                            self.current_menu = None
                            self.game_state = 'playing'
                        elif option.name == 'exit':
                            #("I got to the exit action")
                            # (main_game.current_menu.options)
                            self.current_menu.current_option = 0
                            self.current_menu = None
                            self.game_state = 'playing'

    def main_menu_loop(self):
        while not tdl.event.is_window_closed() and self.game_state == 'main_menu':
            self.main_menu.render_menu(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            self.main_window.blit(self.main_menu.console, 0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            tdl.flush()
            action = self.main_menu.detect_events()
            if action == 'move':
                pass
            elif action == 'select':
                option = self.main_menu.options[self.main_menu.current_option]
                if option.name == 'blank':
                    pass
                elif option.name == 'new':
                    self.game_state = 'playing'
                    return 'new'
                elif option.name == 'load':
                    self.load_game()
                    self.game_state = 'playing'
                    return 'load'
                elif option.name == 'exit':
                    self.game_state = 'exit'
                    return 'exit'

    def save_game(self):
        data = {
             'galaxy' : self.milky_way,
             'player' : self.player,
             'update_time' : self.time_since_last_update,
             'time_elapsed' : self.total_time_elapsed
             }
        with open('saves/save_game.p', 'wb+') as save_file:
            pickle.dump(data, save_file, pickle.HIGHEST_PROTOCOL)

    def load_game(self):
        with open('saves/save_game.p', 'rb') as save_file:
            data = pickle.load(save_file)
            self.milky_way = data['galaxy']
            self.player = data['player']
            self.time_since_last_update = data['update_time']
            self.total_time_elapsed = data['time_elapsed']
        print(self.milky_way)
        print(self.player)

#End of Game Class
main_game = Game()
#("I am before the menu")
main_game.game_state = 'main_menu'
menu_result = main_game.main_menu_loop()
#("I am after the menu")
if menu_result == 'new':
    main_game.generate_galaxy()
    main_game.generate_player_ship()
    main_game.main_loop()
elif menu_result == 'load':
    main_game.main_loop()
elif menu_result == 'exit':
    raise SystemExit('Window closed.')
