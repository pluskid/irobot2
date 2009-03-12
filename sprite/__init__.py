from robot     import SpRobot
from animation import *
from dummy     import SpDummy
from shoot     import SpShoot

import pygame
from   pygame.sprite import Sprite

from util import vec2d

class SpObject(Sprite):
    def __init__(self, position, image):
        Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect().move(position)

