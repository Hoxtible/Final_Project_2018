__author__ = 'yournamehere'
import pygame, math


class Player:
    def __init__(self):
        """
        This is where we set up the variables for this particular object as soon as it is created.
        """
        self.x =  300
        self.y =  300
        self.vx = 0 
        self.vy = 0
        self.angle = 0
        self.i_am_alive = True
        self.left_is_pressed = False
        self.right_is_pressed = False
        self.down_is_pressed = False
        self.up_is_pressed = False
        self.i_am_alive = True
        self.driving_images = []
        self.image = pygame.image.load("player_image.png")
        self.player_turn_direction = 0
    def draw_self(self, surface, world_offset_x, world_offset_y):
        """
        It is this object's responsibility to draw itself on the surface. It will be told to do this often!
        :param surface:
        :return: None
        """
        pygame.draw.rect(surface, pygame.Color("red"), (self.x - 5, self.y - 5, 10, 10))
        surface.blit(self.rotate(),(self.x-10, self.y-10))


    def step(self, delta_T,world_offset_x,world_offset_y):
        """
        In order to change over time, this method gets called very often. The delta_T variable is the amount of time it
        has been since the last time we called "step()" usually about 1/20 -1/60 of a second.
        :param delta_T:
        :return: None
        """
        self.vx = 0
        self.vy = 0

        self.x = self.x + self.vx * delta_T
        self.y = self.y + self.vy * delta_T
        if self.left_is_pressed == True and self.up_is_pressed == False and self.down_is_pressed == False:
            self.angle = 90
        if self.right_is_pressed == True and self.up_is_pressed == False and self.down_is_pressed == False:
            self.angle = 270
        if self.up_is_pressed == True and self.left_is_pressed == False and self.right_is_pressed == False:
            self.angle = 0
        if self.down_is_pressed == True and self.left_is_pressed == False and self.right_is_pressed == False:
            self.angle = 180
        if self.down_is_pressed == True and self.left_is_pressed == True:
            self.angle = 135
        if self.down_is_pressed == True and self.right_is_pressed == True:
            self.angle = 225
        if self.up_is_pressed == True and self.left_is_pressed == True:
            self.angle = 45
        if self.up_is_pressed == True and self.right_is_pressed == True:
            self.angle = 315



    def is_dead(self):

        """
        lets another object know whether this object is still live and on the board. Used by the main loop to clear objects
        in need of removal.
        :return: True or False - is this object dead?
        """
        if self.i_am_alive:
            return False
        else:
            return True
        # alternative (1-line) version of this function:
        #  "return not self.i_am_alive"


    def die(self):
        """
        change the status of this object so that it is dead.
        :return: None
        """
        self.i_am_alive = False

    def rotate(self):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(self.image, self.angle)
        # Get a new rect with the center of the old rect.
        return new_image
