#file for managing all the functions that govern actions
from .system import *
from .sector import Sector
import sys
#TODO: Comment this File Massively
#This will move a ship if possible(returning True) otherwise it will return False

#collision result list:
#destroy: Destroys colliding object
#jump-in: Moves from hyperspace to systemspace
#planet-enter: Moves from systemspace to planetspace
#move: You can move normally, moving on top of the object
#uranium-debug: move next to the station and collect your debug uranium

def attemptMove(ship, galaxy, dx, dy):
    ship.vector.dx + dx
    ship.vector.dy + dy
    move_result = ship.move(ship.location)
    if move_result['result'] == 'jump-in':
        getEntryPosition(ship.x - move_result['target'].x, ship.y - move_result['target'].y, move_result['target'].hyperlimit.radius)
        ship.location.objlist.remove(ship)
        move_result['target'].objlist.append(ship)
        ship.location = move_result['target']
    elif move_result['result'] == 'planet-enter':
        getEntryPosition(ship.x - move_result['target'].x, ship.y - move_result['target'].y, move_result['target'].radius)
        ship.location.objlist.remove(ship)
        move_result['target'].objlist.append(ship)
        ship.location = move_result['target']
    elif move_result['result'] == 'destroy':
        print("You crashed.")
        sys.exit(0)
    elif move_result['result'] == 'uranium-debug':
        dx = 0
        dy = 0
        if ship.x > move_result['target'].x:
            dx = 1
        elif ship.x < move_result['target'].x:
            dx = -1
        if ship.y > move_result['target'].y:
            dy = 1
        elif ship.y < move_result['target'].y:
            dy = -1
    elif move_result['result'] == 'move':
        ship.x += ship.vector.dx
        ship.y += ship.vector.dy
        if isinstance(ship.location, Planet):
            radius = math.sqrt(ship.x*ship.x + ship.y*ship.y)
            if radius >= ship.location.radius:
                vectors = getExitVector(ship.x, ship.y)
                ship.x = ship.location.x + vectors[0]
                ship.y = ship.location.y + vectors[1]
                ship.location.objlist.remove(ship)
                ship.location = ship.location.system
                ship.location.objlist.append(ship)
    
        
        
def getExitVector(x, y):
    dx = 0
    dy = 0
    angle = math.degrees(math.atan(y/x))
    if (angle > 0+22.5) and (angle <= 90-22.5):
        dx = 1
        dy = 1
    elif (angle > 90-22.5) and (angle <= 90+22.5):
        dy = 1
    elif (angle > 90+22.5) and (angle <= 180-22.5):
        dx = -1
        dy = 1
    elif (angle > 180-22.5) and (angle <= 180+22.5):
        dx = -1
    elif (angle > 180+22.5) and (angle <= 270-22.5):
        dx = -1
        dy = -1
    elif (angle > 270-22.5) and (angle <= 270+22.5):
        dy = -1
    elif (angle > 270+22.5) and (angle <= 360-22.5):
        dx = 1
        dy = -1
    else:
        dx = 1
    return (dx, dy)

def getEntryPosition(dx, dy, radius):
    angle = 0
    if (dx == 1) and (dy == 0):
        angle = 0
    elif (dx == 1) and (dy == 1):
        angle = 45
    elif (dx == 0) and (dy == 1):
        angle = 90
    elif (dx == -1) and (dy == 1):
        angle = 135
    elif (dx == -1) and (dy == 0):
        angle = 180
    elif (dx == -1) and (dy == -1):
        angle = 225
    elif (dx == 0) and (dy == -1):
        angle = 270
    elif (dx == 1) and (dy == -1):
        angle = 315
    x = angle*math.cos(radius)
    y = angle*math.sin(radius)
    return (x, y)

#This governs the ship moving through the system level
def systemMove(ship, galaxy, dx, dy):
    #Assumes that the ship's move was successful
    successful_move = True
    entering_planet = False
    #You cannot move into Stars
    if (ship.location.star.x == ship.x+dx) and (ship.location.star.y == ship.y+dy):
        successful_move = False
    else:
        #This checks if the ship is moving into the same space as a planet. If it is, the ship will enter the planets location, its exact entry is dependent on what its relative entry vector is
        if len(ship.location.planetlist) > 0:
            for planet in ship.location.planetlist:
                if (isinstance(planet, Planet)):
                    if (planet.x == ship.x+dx) and (planet.y == ship.y + dy):
                        successful_move = False
                        ship.location.objlist.remove(ship)
                        ship.location = planet
                        ship.location.objlist.append(ship)
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
        #After checking star and planets, check the remaining system objects
        if len(ship.location.system_objects) > 0:
            for obj in ship.location.system_objects:
                if (obj.x == ship.x + dx) and (obj.y == ship.y + dy):
                    #Logic for handling wormholes. Will teleport the ship to the new system
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
    #If the move was successful and you did not enter a planet(This line may need to be updated when new System-Objects are coded) actually move
    if successful_move and not entering_planet:
        ship.move(dx, dy)
        if int(math.pow(math.pow(max(ship.location.star.x, ship.x) - min(ship.location.star.x, ship.x),2) + math.pow(max(ship.location.star.y, ship.y) - min(ship.location.star.y, ship.y), 2), 1/2)) <= ship.sensor_range:
            ship.location.explored = True
        return True
    else:
        return False

#this governs the ship moving through the planet level
def planetMove(ship, galaxy, dx, dy):
    successful_move = True
    #In the planet view the main planet is always at 0,0
    if ship.x+dx == 0 and ship.y+dy == 0:
        successful_move = False
    #check object list
    if len(ship.location.objlist) > 0:
        for obj in ship.location.objlist:
            if (ship.x+dx == obj.x) and ( ship.y+dy == obj.y):
                successful_move = obj.onCollide(ship, dx, dy)
    if len(ship.location.moonlist) > 0:
        for moon in ship.location.moonlist:
            if isinstance(moon, Planet):
                if moon.x == ship.x+dx and moon.y == ship.y + dy:
                    successful_move = False
    #If you can move, move, if you move beyond the planet limit, return to the system view
    if successful_move:
        distance_from_planet = math.pow((math.pow(ship.x, 2)) + (math.pow(ship.y, 2)), 1/2.0)
        if distance_from_planet >= ship.location.planet_limit.radius + 1:
            #math governing where in the system view you return too
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
            #change location;
            ship.location.objlist.remove(ship)
            ship.location = ship.location.system
            ship.location.objlist.append(ship)
            return True
        else:
            #Otherwise just do a normal move
            ship.move(dx, dy)
            return True
    else:
        return False


#this governs the ship moving through the sector level
def sectorMove(ship, galaxy, dx, dy):
    successful_move = True
    entering_system = False
    #if in a sector with systems, check to see if you collide with a system
    if len(ship.location.systemlist) > 0:
        for system in ship.location.systemlist:
            if (system.x == ship.x+dx) and (system.y == ship.y + dy):
                #if you collide with a system, enter it
                entering_system = True
                if ship.player:
                    ship.ui.message("Entering " + system.name, 'helm')
                ship.location.objlist.remove(ship)
                ship.location = system
                ship.location.objlist.append(ship)
                has_wormhole = False
                for sysobj in ship.location.system_objects:
                    if isinstance(sysobj, Wormhole):
                        has_wormhole = True
                #If the system has a wormhole, tell the player
                if has_wormhole:
                    if ship.player:
                        ship.ui.message("", 'helm')#needed to ensure messages don't break
                        ship.ui.message("I am detecting a gravitational anomaly.", 'science')
                    for msg in ship.ui.msgs:
                        pass
                        #(msg)
                #Do math to figure out where in the system you appear
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
                #end math
    if successful_move and not entering_system:
        #Move yourself, then see if your still in your sector. If you are not, get the new sector and move yourself to it
        ship.move(dx, dy)
        lessthanx = ship.x < ship.location.x*ship.location.width
        lessthany = ship.y < ship.location.y*ship.location.height
        greaterthanx = ship.x > (ship.location.x+1)*ship.location.width-1
        greaterthany = ship.y > (ship.location.y+1)*ship.location.height-1
        if lessthanx and lessthany:
            ship.location.objlist.remove(ship)
            ship.location = galaxy.get_sector(ship.location, -1, -1)
            ship.location.objlist.append(ship)
            return True
        elif lessthanx and greaterthany:
            ship.location.objlist.remove(ship)
            ship.location = galaxy.get_sector(ship.location, -1, 1)
            ship.location.objlist.append(ship)
            return True
        elif greaterthanx and lessthany:
            ship.location.objlist.remove(ship)
            ship.location = galaxy.get_sector(ship.location, 1, -1)
            ship.location.objlist.append(ship)
            return True
        elif greaterthanx and greaterthany:
            ship.location.objlist.remove(ship)
            ship.location = galaxy.get_sector(ship.location, 1, 1)
            ship.location.objlist.append(ship)
            return True
        elif greaterthanx and not lessthany and not greaterthany:
            ship.location.objlist.remove(ship)
            ship.location = galaxy.get_sector(ship.location, 1, 0)
            ship.location.objlist.append(ship)
            return True
        elif lessthanx and not lessthany and not greaterthany:
            ship.location.objlist.remove(ship)
            ship.location = galaxy.get_sector(ship.location, -1, 0)
            ship.location.objlist.append(ship)
            return True
        elif greaterthany and not lessthanx and not greaterthanx:
            ship.location.objlist.remove(ship)
            ship.location = galaxy.get_sector(ship.location, 0, 1)
            ship.location.objlist.append(ship)
            return True
        elif lessthany and not lessthanx and not greaterthanx:
            ship.location.objlist.remove(ship)
            ship.location = galaxy.get_sector(ship.location, 0, -1)
            ship.location.objlist.append(ship)
            return True
        return True
    else:
        return False


#this code governs if a ship can jump out of a solar sytem
def attemptJump(ship, clock):
    if not isinstance(ship.location, System):
        if isinstance(ship.location, Planet):
            #you cannot jump from within a planet's influence
            if ship.player:
                ship.ui.message("Too close to planet to jump", "helm")
        else:
            return False
    else:
        #You cannot jump if you are within a planets hyperlimit
        distance_from_star = math.pow((math.pow(ship.x, 2)) + (math.pow(ship.y, 2)), 1/2.0)
        if distance_from_star >= ship.location.hyperlimit.radius:
            #if we do jump, tell them we are jumping
            if ship.player:
                ship.ui.message("Jumping to hyperspace",  'helm')
                #math to find out where in the secto we appear
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
            ship.location.objlist.remove(ship)
            ship.location = ship.location.sector
            ship.location.objlist.append(ship)
        else:
            #Tell the player why the jump failed if it did
            if ship.player:
                ship.ui.message("Jump failed, too close to star", 'helm')
