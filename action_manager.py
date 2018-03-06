#file for managing all the functions that govern actions
from system import *
from sector import Sector

def attemptMove(ship, galaxy, dx, dy):
    entering_planet = False
    if ship.location == None:
        ship.move(dx, dy)
        return True
    elif isinstance(ship.location, System):
        successful_move = True
        if (ship.location.star.x == ship.x+dx) and (ship.location.star.y == ship.y+dy):
            successful_move = False
        else:
            if len(ship.location.planetlist) > 0:
                for planet in ship.location.planetlist:
                    if (isinstance(planet, Planet)):
                        if (planet.x == ship.x+dx) and (planet.y == ship.y + dy):
                            successful_move = False
                            ship.location = planet
                            entering_planet = True
                            if dx == -1 and dy == 0:
                                ship.x = 1*ship.location.planet_limit.radius
                                ship.y = 0*ship.location.planet_limit.radius
                                return True
                            elif dx == -1 and dy == -1:
                                ship.x = int((math.pow(2,1/2)/2)*ship.location.planet_limit.radius)
                                ship.y = int((math.pow(2,1/2)/2)*ship.location.planet_limit.radius)
                                return True
                            elif dx == 0 and dy == 1:
                                ship.x = 0*ship.location.planet_limit.radius
                                ship.y = -1*ship.location.planet_limit.radius
                                return True
                            elif dx == 1 and dy == 1:
                                ship.x = -1*int((math.pow(2,1/2)/2)*ship.location.planet_limit.radius)
                                ship.y = -1*int((math.pow(2,1/2)/2)*ship.location.planet_limit.radius)
                                return True
                            elif dx == 1 and dy == 0:
                                ship.x = -1*ship.location.planet_limit.radius
                                ship.y = 0*ship.location.planet_limit.radius
                                return True
                            elif dx == 1 and dy == -1:
                                ship.x = -1*int((math.pow(2,1/2)/2)*ship.location.planet_limit.radius)
                                ship.y = int((math.pow(2,1/2)/2)*ship.location.planet_limit.radius)
                                return True
                            elif dx == 0 and dy == -1:
                                ship.x = 0*ship.location.planet_limit.radius
                                ship.y = 1*ship.location.planet_limit.radius
                                return True
                            elif dx == -1 and dy == 1:
                                ship.x = int((math.pow(2,1/2)/2)*ship.location.planet_limit.radius)
                                ship.y = -1*int((math.pow(2,1/2)/2)*ship.location.planet_limit.radius)
                                return True
                            break
            if len(ship.location.system_objects) > 0:
                for obj in ship.location.system_objects:
                    if (obj.x == ship.x + dx) and (obj.y == ship.y + dy):
                        if isinstance(obj, Wormhole):
                            if obj.destination == None:
                                exit_wormhole = obj.generate_destination(galaxy, ship.location.sector)
                            else:
                                exit_wormhole = obj.destination
                            ship.location = exit_wormhole.system
                            if ship.player:
                                ship.ui.message("Entering " + ship.location.name, 'helm')
                            ship.x = exit_wormhole.x + dx
                            ship.y = exit_wormhole.y + dy
                            successful_move = False
                            return True
                        else:
                            successful_move = False
                            return False
                    else:
                        successful_move = True
        if successful_move and not entering_planet:
            ship.move(dx, dy)
            if int(math.pow(math.pow(max(ship.location.star.x, ship.x) - min(ship.location.star.x, ship.x),2) + math.pow(max(ship.location.star.y, ship.y) - min(ship.location.star.y, ship.y), 2), 1/2)) <= ship.sensor_range:
                ship.location.explored = True
            return True
        else:
            return False
    elif isinstance(ship.location, Planet):
        successful_move = True
        if ship.x+dx == 0 and ship.y+dy == 0:
            successful_move = False
        else:
            if len(ship.location.moonlist) > 0:
                for moon in ship.location.moonlist:
                    if isinstance(moon, Planet):
                        if moon.x == ship.x+dx and moon.y == ship.y + dy:
                            successful_move = False
        if successful_move:
            distance_from_planet = math.pow((math.pow(ship.x, 2)) + (math.pow(ship.y, 2)), 1/2)
            if distance_from_planet >= ship.location.planet_limit.radius + 1:
                if ship.x > 0 and ship.y == 0:
                    ship.x = ship.location.x + 1
                    ship.y = ship.location.y
                elif ship.x == 0 and ship.y > 0:
                    ship.x = ship.location.x
                    ship.y = ship.location.y + 1
                elif ship.x < 0 and ship.y == 0:
                    ship.x = ship.location.x - 1
                    ship.y = ship.location.y
                elif ship.x == 0 and ship.y < 0:
                    ship.x = ship.location.x
                    ship.y = ship.location.y - 1
                elif ship.x < 0 and ship.y < 0:
                    theta = math.degrees(math.atan(ship.x/ship.y))
                    if theta > 90 - 22.5:
                        ship.x = ship.location.x - 1
                        ship.y = ship.location.y
                    elif theta < 0 + 22.5:
                        ship.x = ship.location.x
                        ship.y = ship.location.y - 1
                    else:
                        ship.x = ship.location.x - 1
                        ship.y = ship.location.y - 1
                elif ship.x > 0 and ship.y > 0:
                    theta = math.degrees(math.atan(ship.x/ship.y))
                    if theta > 90 - 22.5:
                        ship.x = ship.location.x + 1
                        ship.y = ship.location.y
                    elif theta < 0 + 22.5:
                        ship.x = ship.location.x
                        ship.y = ship.location.y + 1
                    else:
                        ship.x = ship.location.x + 1
                        ship.y = ship.location.y + 1
                elif ship.x < 0 and ship.y > 0:
                    theta = math.degrees(math.atan(ship.x/ship.y))
                    if theta < -90 + 22.5:
                        ship.x = ship.location.x - 1
                        ship.y = ship.location.y
                    elif theta > 0 - 22.5:
                        ship.x = ship.location.x
                        ship.y = ship.location.y + 1
                    else:
                        ship.x = ship.location.x - 1
                        ship.y = ship.location.y + 1
                elif ship.x > 0 and ship.y < 0:
                    theta = math.degrees(math.atan(ship.x/ship.y))
                    if theta > 0 - 22.5:
                        ship.x = ship.location.x
                        ship.y = ship.location.y - 1
                    elif theta < -90 + 22.5:
                        ship.x = ship.location.x + 1
                        ship.y = ship.location.y
                    else:
                        ship.x = ship.location.x + 1
                        ship.y = ship.location.y - 1
                ship.location = ship.location.system
                return True
            else:
                ship.move(dx, dy)
                return True
        else:
            return False
    elif isinstance(ship.location, Sector):
        successful_move = True
        entering_system = False
        if len(ship.location.systemlist) > 0:
            for system in ship.location.systemlist:
                if (system.x == ship.x+dx) and (system.y == ship.y + dy):
                    entering_system = True
                    if ship.player:
                        ship.ui.message("Entering " + system.name, 'helm')
                    ship.location = system
                    has_wormhole = False
                    for sysobj in ship.location.system_objects:
                        if isinstance(sysobj, Wormhole):
                            has_wormhole = True
                    if has_wormhole:
                        if ship.player:
                            ship.ui.message("", 'helm')
                            ship.ui.message("I am detecting a gravitational anomaly.", 'science')
                        for msg in ship.ui.msgs:
                            print(msg)
                    if dx == -1 and dy == 0:
                        ship.x = 1*ship.location.hyperlimit.radius
                        ship.y = 0*ship.location.hyperlimit.radius
                        return True
                    elif dx == -1 and dy == -1:
                        ship.x = int((math.pow(2,1/2)/2)*ship.location.hyperlimit.radius)
                        ship.y = int((math.pow(2,1/2)/2)*ship.location.hyperlimit.radius)
                        return True
                    elif dx == 0 and dy == 1:
                        ship.x = 0*ship.location.hyperlimit.radius
                        ship.y = -1*ship.location.hyperlimit.radius
                        return True
                    elif dx == 1 and dy == 1:
                        ship.x = -1*int((math.pow(2,1/2)/2)*ship.location.hyperlimit.radius)
                        ship.y = -1*int((math.pow(2,1/2)/2)*ship.location.hyperlimit.radius)
                        return True
                    elif dx == 1 and dy == 0:
                        ship.x = -1*ship.location.hyperlimit.radius
                        ship.y = 0*ship.location.hyperlimit.radius
                        return True
                    elif dx == 1 and dy == -1:
                        ship.x = -1*int((math.pow(2,1/2)/2)*ship.location.hyperlimit.radius)
                        ship.y = int((math.pow(2,1/2)/2)*ship.location.hyperlimit.radius)
                        return True
                    elif dx == 0 and dy == -1:
                        ship.x = 0*ship.location.hyperlimit.radius
                        ship.y = 1*ship.location.hyperlimit.radius
                        return True
                    elif dx == -1 and dy == 1:
                        ship.x = int((math.pow(2,1/2)/2)*ship.location.hyperlimit.radius)
                        ship.y = -1*int((math.pow(2,1/2)/2)*ship.location.hyperlimit.radius)
                        return True
                    break
        if successful_move and not entering_system:
            ship.move(dx, dy)
            lessthanx = ship.x < ship.location.x*ship.location.width
            lessthany = ship.y < ship.location.y*ship.location.height
            greaterthanx = ship.x > (ship.location.x+1)*ship.location.width-1
            greaterthany = ship.y > (ship.location.y+1)*ship.location.height-1
            if lessthanx and lessthany:
                ship.location = galaxy.get_sector(ship.location, -1, -1)
                return True
            elif lessthanx and greaterthany:
                ship.location = galaxy.get_sector(ship.location, -1, 1)
                return True
            elif greaterthanx and lessthany:
                ship.location = galaxy.get_sector(ship.location, 1, -1)
                return True
            elif greaterthanx and greaterthany:
                ship.location = galaxy.get_sector(ship.location, 1, 1)
                return True
            elif greaterthanx and not lessthany and not greaterthany:
                ship.location = galaxy.get_sector(ship.location, 1, 0)
                return True
            elif lessthanx and not lessthany and not greaterthany:
                ship.location = galaxy.get_sector(ship.location, -1, 0)
                return True
            elif greaterthany and not lessthanx and not greaterthanx:
                ship.location = galaxy.get_sector(ship.location, 0, 1)
                return True
            elif lessthany and not lessthanx and not greaterthanx:
                ship.location = galaxy.get_sector(ship.location, 0, -1)
                return True
            return True
        else:
            return False

def attemptJump(ship, clock):
    if not isinstance(ship.location, System):
        if isinstance(ship.location, Planet):
            if ship.player:
                ship.ui.message("Too close to planet to jump", "helm")
        else:
            return False
    else:
        distance_from_star = math.pow((math.pow(ship.x, 2)) + (math.pow(ship.y, 2)), 1/2)
        if distance_from_star >= ship.location.hyperlimit.radius:
            if ship.player:
                ship.ui.message("Jumping to hyperspace",  'helm')
            if ship.x > 0 and ship.y == 0:
                ship.x = ship.location.x + 1
                ship.y = ship.location.y
            elif ship.x == 0 and ship.y > 0:
                ship.x = ship.location.x
                ship.y = ship.location.y + 1
            elif ship.x < 0 and ship.y == 0:
                ship.x = ship.location.x - 1
                ship.y = ship.location.y
            elif ship.x == 0 and ship.y < 0:
                ship.x = ship.location.x
                ship.y = ship.location.y - 1
            elif ship.x < 0 and ship.y < 0:
                theta = math.degrees(math.atan(ship.x/ship.y))
                if theta > 90 - 22.5:
                    ship.x = ship.location.x - 1
                    ship.y = ship.location.y
                elif theta < 0 + 22.5:
                    ship.x = ship.location.x
                    ship.y = ship.location.y - 1
                else:
                    ship.x = ship.location.x - 1
                    ship.y = ship.location.y - 1
            elif ship.x > 0 and ship.y > 0:
                theta = math.degrees(math.atan(ship.x/ship.y))
                if theta > 90 - 22.5:
                    ship.x = ship.location.x + 1
                    ship.y = ship.location.y
                elif theta < 0 + 22.5:
                    ship.x = ship.location.x
                    ship.y = ship.location.y + 1
                else:
                    ship.x = ship.location.x + 1
                    ship.y = ship.location.y + 1
            elif ship.x < 0 and ship.y > 0:
                theta = math.degrees(math.atan(ship.x/ship.y))
                if theta < -90 + 22.5:
                    ship.x = ship.location.x - 1
                    ship.y = ship.location.y
                elif theta > 0 - 22.5:
                    ship.x = ship.location.x
                    ship.y = ship.location.y + 1
                else:
                    ship.x = ship.location.x - 1
                    ship.y = ship.location.y + 1
            elif ship.x > 0 and ship.y < 0:
                theta = math.degrees(math.atan(ship.x/ship.y))
                if theta > 0 - 22.5:
                    ship.x = ship.location.x
                    ship.y = ship.location.y - 1
                elif theta < -90 + 22.5:
                    ship.x = ship.location.x + 1
                    ship.y = ship.location.y
                else:
                    ship.x = ship.location.x + 1
                    ship.y = ship.location.y - 1
            ship.location = ship.location.sector
        else:
            if ship.player:
                ship.ui.message("Jump failed, too close to star", 'helm')
