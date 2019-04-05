from .sector import *
import copy
#TODO: add seed
#TODO test this file
class Galaxy:
    def __init__(self):
        self.sectorlist = {}
        self.factions = []
        #TODO: Add SystemGenerator here

    def add_sector(self, sector):
        self.sectorlist[(sector.x, sector.y)] = sector

    def get_sector(self, sector, dx, dy):
        key = (sector.x + dx, sector.y + dy)
        location = self.sectorlist.get(key)
        if location == None:
            new_sector = Sector( "Sector " + str(sector.x+dx) + ", " + str(-(sector.y+dy)), 'normal', sector.x+dx, sector.y+dy, sector.width, sector.height, sector.sysnames)
            new_sector.generate()
            self.add_sector(new_sector)
            location = new_sector
        return location

    def sector_draw(self, sector, console, topx, topy, sw, sh):
        for x in range(-1, 2):
            for y in range(-1, 2):
                draw_sector = self.get_sector(sector, x, y)
                draw_sector.draw(console, topx, topy, sw, sh)

    def sector_clear(self, sector, console, topx, topy, sw, sh):
        for x in range(sector.x-1, sector.x+1):
            for y in range(sector.y-1, sector.y+1):
                clear_sector = self.get_sector(sector, x, y)
                clear_sector.clear(console, topx, topy, sw, sh)