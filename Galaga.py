'''
Michelle Bartolotta
Python Galaga

YouTube video: https://youtu.be/jEGALOTOUw0

'''
from dataclasses import dataclass
from designer import *
from random import randint

SHIP_SPEED = 0
ALIEN_SPEED = 4
LASER_SPEED = 4
game_over_x_coord = (get_width() / 2)
game_over_y_coord = (get_height() / 2) +50
ending_text = text("white","", 20,400,180)

@dataclass
class World:
    background:DesignerObject
    ship: DesignerObject
    ship_speed: int
    lives: int
    score:int
    aliens: list[DesignerObject]
    counter: DesignerObject
    lasers: list[DesignerObject]
    explosions: list[DesignerObject]
    
def create_ship() -> DesignerObject:
    """ Create the ship """
    ship = emoji("rocket")
    ship.y = get_height() * (2 / 3)
    ship.flip_x = True
    return ship

def create_world() -> World:
    """ Create the world """
    game_over_x_coord = (get_width() / 2)
    game_over_y_coord = (get_height() / 2)
    return World(rectangle('black', 1000, 1000),create_ship(),SHIP_SPEED,3,0,[],text("white", "", 20, game_over_x_coord, game_over_y_coord),[],[])

def move_ship(world: World):
    """ Move the ship horizontally"""  
    world.ship.x += world.ship_speed
    
def bounce_ship(world: World):
    """ Handle the ship bouncing off a wall """
    if world.ship.x > get_width():
        head_left(world)
    elif world.ship.x < 0:
        head_right(world)
    
def head_left(world: World):
    """ Make the ship start moving left """
    world.ship.x += -5
    world.ship.flip_x = True
    
def head_right(world: World):
    """ Make the ship start moving left """
    world.ship.x += 5
    world.ship.flip_x = False
    
def flip_ship(world: World, key: str):
    """ Change the direction that the ship is moving """
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)

def typing(world: World, key: str):
    if key == "left":
        world.ship_speed = -5
    if key == 'right':
        world.ship_speed = 5
    
def done_typing(world: World, key: str):
    world.ship_speed = 0
    
def create_alien() -> DesignerObject:
    """Create the alien and put them at a random spot"""
    alien = emoji("👾")
    alien.anchor = 'midbottom'
    alien.x = randint(0, 800)
    alien.y = 0
    return alien

def make_aliens(world:World):
    """Always have there be 6 aliens"""
    if len(world.aliens) < 6:
        world.aliens.append(create_alien())

def make_alien_fall(world: World):
    '''make aliens fall'''
    for alien in world.aliens:
        alien.y += ALIEN_SPEED

def alien_wrap(world:World):
    """aliens will wrap up to the top of the screen"""
    for alien in world.aliens:
        if alien.y > 640:
            alien.y = 10

def collide_alien_ship(world:World)->bool:
    """if the alien and ship collide, the ship will lose a life, if all lives are gone it will game over"""
    show_game_over = False
    for alien in world.aliens:
        if colliding(alien, world.ship):      
            if world.lives == 0:
                show_game_over = True
                ending_text = text("white","Game Over", 20,400,380)
                #Explosion emoji shows on ship when the ship dies
                explosion = emoji('💥')
                explosion.x = world.ship.x
                explosion.y = world.ship.y
            else:
                world.lives -= 1
                for alien in world.aliens:
                    alien.y = 10
        world.counter.text = "Score: " + str(world.score) + " Lives: " + str(world.lives)
    return show_game_over

def create_laser() -> DesignerObject:
    '''create a laser'''
    return ellipse('white', 5, 10)

def shoot_laser(world: World, key: str):
    """ Create a laser when the space bar is pressed """
    if key == 'space':
        new_laser = create_laser()
        move_above(world.ship, new_laser)
        world.lasers.append(new_laser)

def move_above(bottom: DesignerObject, top: DesignerObject):
    """ Move the top to be above the bottom object """
    top.y = bottom.y + bottom.height/-2
    top.x = bottom.x
        
def make_laser_fly(world: World):
    """ Move the laser up """
    for laser in world.lasers:
        laser.y -= LASER_SPEED
        
def destroy_lasers_at_top(world: World):
    """ Destroy any lasers that go offscreen """
    kept = []
    for laser in world.lasers:
        if laser.y < get_height():
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept
    
def collide_laser_alien(world: World):
    destroyed_lasers = []
    destroyed_aliens = []
    # Compare every laser to every alien
    for laser in world.lasers:
        for alien in world.aliens:
            # update score and show explosion if laser and alien collide
            if colliding(laser, alien):
                world.explosions.append(create_explosion(alien))
                destroyed_lasers.append(laser)
                destroyed_aliens.append(alien)
                world.score += 1              
    # Remove any lasers/aliens that were identified as colliding
    world.lasers = filter_from(world.lasers, destroyed_lasers)
    world.aliens = filter_from(world.aliens, destroyed_aliens)
    
def create_explosion(alien:DesignerObject) -> DesignerObject:
    '''creates an explosion and positions it to be where the alien is'''
    explosion = emoji('💥')
    explosion.x = alien.x
    explosion.y = alien.y
    return explosion
    
def hide_explosion(world:World):
    '''hides explosions after they are shown'''
    for explosion in world.explosions:
        if explosion:
            hide(explosion)
            
def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values

when('starting', create_world)
when("updating", move_ship)
when("updating", bounce_ship)
when("typing", typing)
when('done typing', done_typing)
when("typing", flip_ship)
when('updating', hide_explosion)
when('typing', shoot_laser)
when('updating', make_laser_fly)
when("updating", make_aliens)
when('updating', make_alien_fall)
when("updating", destroy_lasers_at_top)
when('updating', collide_laser_alien)
when('updating', alien_wrap)
when('updating', collide_alien_ship)
when(collide_alien_ship,pause)

start()
