__author__ = 'yournamehere'
import pygame, random


class Enemy:
    def __init__(self):
        """
        This is where we set up the variables for this particular object as soon as it is created.
        """
        self.x = 0
        self.y = 0
        self.vx = random.randrange(50,500)
        self.vy = random.randrange(50,500)
        self.i_am_alive = True
        self.location_x = 0
        self.location_y = 0
    def draw_self(self, surface, world_offset_x, world_offset_y):
        """
        It is this object's responsibility to draw itself on the surface. It will be told to do this often!
        :param surface:
        :return: None
        """
        pygame.draw.rect(surface, pygame.Color("green"), (self.x - world_offset_x - 5, self.y -world_offset_y -5, 10, 10))

    def step(self, delta_T, world_offset_x, world_offset_y):
        """
        In order to change over time, this method gets called very often. The delta_T variable is the amount of time it
        has been since the last time we called "step()" usually about 1/20 -1/60 of a second.
        :param delta_T:
        :return: None
        """
        self.location_x = self.x - world_offset_x - 5
        self.location_y = self.y - world_offset_y - 5
        self.x = self.x + self.vx * delta_T
        self.y = self.y + self.vy * delta_T
        if self.location_x < 0 - world_offset_x +300 - 5:
            self.vx = abs(self.vx) * 1


        if self.location_x >1200 - world_offset_x +300 - 5:
            self.vx = abs(self.vx) * -1


        if self.location_y < 0 - world_offset_y +300 - 5:
            self.vy = abs(self.vy) * 1



        if self.location_y > 1200 - world_offset_y +300 - 5:
            self.vy = abs(self.vy) * -1

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