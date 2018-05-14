__author__ = 'yournamehere'  # put your name here!!!

import pygame, sys, traceback, random
from pygame.locals import *

GAME_MODE_MAIN = 0
GAME_MODE_TITLE_SCREEN = 1

# import your classFiles here.
from pygame_player import Player
from pygame_bullet import Bullet
from pygame_enemy  import Enemy

# =====================  setup()
def setup():
    global player, bullet
    """
    This happens once in the program, at the very beginning.
    """
    global buffer, objects_on_screen, objects_to_add, bg_color, game_mode, world_offset_x, world_offset_y,space_background, bullet_list, enemy_list
    global score

    buffer = pygame.display.set_mode((600, 600))
    objects_on_screen = []  # this is a list of all things that should be drawn on screen.
    objects_to_add = [] #this is a list of things that should be added to the list on screen. Put them here while you
                        #   are in the middle of the loop, and they will be added in later in the loop, when it is safe
                        #   to do so.
    bg_color = pygame.Color("royalblue4")  # you can find a list of color names at https://goo.gl/KR7Pke
    game_mode = GAME_MODE_MAIN
    player = Player()
    objects_on_screen.append(player)
    # Add any other things you would like to have the program do at startup here.
    x = 0
    world_offset_y = 300
    world_offset_x = 300
    space_background = pygame.image.load("space_background.jpg")
    bullet_list = []
    enemy_list = []
    score = 0
    for i in range(10):
        new_enemy = Enemy()
        enemy_list.append(new_enemy)
        objects_on_screen.append(new_enemy)

# =====================  loop()
def loop(delta_T):
    global space_background, world_offset_x, world_offset_y
    """
     this is what determines what should happen over and over.
     delta_T is the time (in seconds) since the last loop() was called.
    """
    buffer.blit(space_background, (-(world_offset_x / 2 % 1221), -(world_offset_y / 2 % 1221)))
    if (world_offset_x / 2 % 1221) > 1221:
        buffer.blit(space_background, (1220 - (world_offset_x / 2 % 1221), 1220 - (world_offset_y / 2 % 1221)))

    if game_mode == GAME_MODE_MAIN:
        animate_objects(delta_T)

        move_player(delta_T)
        bounds_check_player()
        check_for_collision()



        print(world_offset_y,",",world_offset_x)


        # place any other code to test interactions between objects here. If you want them to
        # disappear, set them so that they respond True to isDead(), and they will be deleted next. If you want to put
        # more objects on screen, add them to the global variable objects_to_add, and they will be added later in this
        # loop.


        clear_dead_objects()
        add_new_objects()
        draw_objects()
        show_stats(delta_T) #optional. Comment this out if it annoys you.
    pygame.display.flip()  # updates the window to show the latest version of the buffer.


def shoot():
    bullet = Bullet()
    global objects_on_screen, bullet_list, world_offset_y, world_offset_x
    if player.left_is_pressed == False and player.up_is_pressed == False and player.down_is_pressed == False and player.right_is_pressed == False:
        return

    if player.left_is_pressed == True and player.up_is_pressed == False and player.down_is_pressed == False:
        bullet.x = player.x + world_offset_x
        bullet.y = player.y + world_offset_y
        bullet.vx = -300
        bullet.vy = 0
    if player.right_is_pressed == True and player.up_is_pressed == False and player.down_is_pressed == False:
        bullet.x = player.x + world_offset_x
        bullet.y = player.y + world_offset_y
        bullet.vx = 300
        bullet.vy = 0
    if player.up_is_pressed == True and player.left_is_pressed == False and player.right_is_pressed == False:
        bullet.x = player.x + world_offset_x
        bullet.y = player.y + world_offset_y
        bullet.vx = 0
        bullet.vy = -300
    if player.down_is_pressed == True and player.left_is_pressed == False and player.right_is_pressed == False:
        bullet.x = player.x + world_offset_x
        bullet.y = player.y + world_offset_y
        bullet.vx = 0
        bullet.vy = 300
    if player.down_is_pressed == True and player.left_is_pressed == True:
        bullet.x = player.x + world_offset_x
        bullet.y = player.y + world_offset_y
        bullet.vx = -300
        bullet.vy = 300
    if player.down_is_pressed == True and player.right_is_pressed == True:
        bullet.x = player.x + world_offset_x
        bullet.y = player.y + world_offset_y
        bullet.vx = 300
        bullet.vy = 300
    if player.up_is_pressed == True and player.left_is_pressed == True:
        bullet.x = player.x + world_offset_x
        bullet.y = player.y + world_offset_y
        bullet.vx = -300
        bullet.vy = -300
    if player.up_is_pressed == True and player.right_is_pressed == True:
        bullet.x = player.x + world_offset_x
        bullet.y = player.y + world_offset_y
        bullet.vx = 300
        bullet.vy = -300
    bullet_list.append(bullet)
    objects_on_screen.append(bullet)
def check_for_collision():
    global bugs_shot, bullet_list, enemy_list, objects_on_screen, shootyboi, score
    for bullet in bullet_list:
        for enemy in enemy_list:
            if abs((bullet.x - 0) - (enemy.x - 0)) <= 12 and abs((bullet.y - 0) - (enemy.y - 0)) <= 12:
                bullet.die()
                enemy.die()
                score += 10

def move_player(delta_T):
    global space_background, world_offset_x, world_offset_y

    if player.right_is_pressed and world_offset_x <= 1199:
        world_offset_x = world_offset_x + 200 * delta_T
        player.right_is_pressed = True
    else:
        player.right_is_pressed = False

    if player.left_is_pressed and world_offset_x >= 1:
        world_offset_x = world_offset_x - 200 * delta_T
        player.left_is_pressed = True
    else:
        player.left_is_pressed = False

    if player.down_is_pressed and world_offset_y <= 1199:
        world_offset_y = world_offset_y + 200 * delta_T
        player.down_is_pressed = True
    else:
        player.down_is_pressed = False

    if player.up_is_pressed and world_offset_y >= 1:
        world_offset_y = world_offset_y - 200 * delta_T
        player.up_is_pressed = True
    else:
        player.up_is_pressed = False
def bounds_check_player():
    global world_offset_x, world_offset_y
    if world_offset_y < 0:
        world_offset_y = 1
    if world_offset_x < 0:
        world_offset_x = 1
    if world_offset_y > 1200:
        world_offset_y = 1199
    if world_offset_x > 1200:
        world_offset_x = 1199



# =====================  animate_objects()
def animate_objects(delta_T):
    """
    tells each object to "step"...
    """
    global objects_on_screen, world_offset_x, world_offset_y
    for object in objects_on_screen:
        if object.is_dead(): #   ...but don't bother "stepping" the dead ones.
            continue
        object.step(delta_T,world_offset_x,world_offset_y)


# =====================  clear_dead_objects()
def clear_dead_objects():
    """
    removes all objects that are dead from the "objectsOnScreen" list
    """
    global objects_on_screen, enemy_list, bullet_list
    i = 0
    for object in objects_on_screen[:]:
        if object.is_dead():
            objects_on_screen.pop(i) # removes the ith object and pulls everything else inwards, so don't advance "i"
                                     #      ... they came back to you.
        else:
            i += 1
    i = 0
    for bullet in bullet_list[:]:
        if bullet.is_dead():
            bullet_list.pop(i)
        else:
            i+=1
    i = 0
    for enemy in enemy_list[:]:
        if enemy.is_dead():
            enemy_list.pop(i)
        else:
            i += 1


# =====================  add_new_objects()
def add_new_objects():
    """
    Adds all the objects in the list "objects to add" to the list of "objects on screen" and then clears the "to add" list.
    :return: None
    """
    global objects_to_add, objects_on_screen
    objects_on_screen.extend(objects_to_add)
    objects_to_add.clear()

# =====================  draw_objects()
def draw_objects():
    """
    Draws each object in the list of objects.
    """
    global world_offset_x, world_offset_y
    for object in objects_on_screen:
        object.draw_self(buffer, world_offset_x, world_offset_y)


# =====================  show_stats()
def show_stats(delta_T):
    global score
    """
    draws the frames-per-second in the lower-left corner and the number of objects on screen in the lower-right corner.
    Note: the number of objects on screen may be a bit misleading. They still count even if they are being drawn off the
    edges of the screen.
    :param delta_T: the time since the last time this loop happened, used to calculate fps.
    :return: None
    """
    white_color = pygame.Color(255,255,255)
    stats_font = pygame.font.SysFont('Arial', 10)
    score_string = score

    fps_string = "FPS: {0:3.1f}".format(1.0/delta_T) #build a string with the calculation of FPS.
    fps_text_surface = stats_font.render(fps_string,True,white_color) #this makes a transparent box with text
    fps_text_rect = fps_text_surface.get_rect()   # gets a copy of the bounds of the transparent box
    fps_text_rect.left = 10  # now relocate the box to the lower left corner
    fps_text_rect.bottom = buffer.get_rect().bottom - 10
    buffer.blit(fps_text_surface, fps_text_rect) #... and copy it to the buffer at the location of the box

    objects_string = "Objects: {0:5d}".format(len(objects_on_screen)) #build a string with the number of objects
    objects_text_surface = stats_font.render(objects_string,True,white_color)
    objects_text_rect = objects_text_surface.get_rect()
    objects_text_rect.right = buffer.get_rect().right - 10 # move this box to the lower right corner
    objects_text_rect.bottom = buffer.get_rect().bottom - 10
    buffer.blit(objects_text_surface, objects_text_rect)

    score_string = "Score: {0}".format(score_string)  # build a string with the number of objects
    score_text_surface = stats_font.render(score_string, True, white_color)
    score_text_rect = score_text_surface.get_rect()
    score_text_rect.left = buffer.get_rect().left + 10  # move this box to the lower right corner
    score_text_rect.top = buffer.get_rect().top + 10
    buffer.blit(score_text_surface, score_text_rect)

# =====================  read_events()
def read_events():
    """
    checks the list of events and determines whether to respond to one.
    """
    events = pygame.event.get()  # get the list of all events since the last time
    for evt in events:
        if evt.type == QUIT:
            pygame.quit()
            raise Exception("User quit the game")
            # You may decide to check other events, like the mouse
            # or keyboard here.
        if evt.type == KEYDOWN:
            player.vx = 0
            player.vy = 0
            if evt.key == K_a:
                player.left_is_pressed = True
            if evt.key == K_d:
                player.right_is_pressed = True
            if evt.key == K_w:
                player.up_is_pressed = True
            if evt.key == K_s:
                player.down_is_pressed = True
            if evt.key == K_SPACE:
                shoot()
        if evt.type == KEYUP:
            player.vx = 0
            player.vy = 0
            if evt.key == K_a:
                player.left_is_pressed = False
            if evt.key == K_d:
                player.right_is_pressed = False
            if evt.key == K_w:
                player.up_is_pressed = False
            if evt.key == K_s:
                player.down_is_pressed = False


# program start with game loop - this is what makes the loop() actually loop.
pygame.init()
try:
    setup()
    fpsClock = pygame.time.Clock()  # this will let us pass the deltaT to loop.
    while True:
        time_since_last_loop = fpsClock.tick(60) / 1000.0 # we set this to go up to as much as 60 fps, probably less.
        loop(time_since_last_loop)
        read_events()

except Exception as reason: # If the user quit, exit gracefully. Otherwise, explain what happened.
    if len(reason.args)>0 and reason.args[0] == "User quit the game":
        print ("Game Over.")
    else:
        traceback.print_exc()
