import pygame

from util import vec2d
from animation import *
from dummy     import SpDummy
from robot     import SpRobot
from shoot     import SpShoot
from basic     import SpBase


class SpObject(SpBase):
    def __init__(self, position, image):
        SpBase.__init__(self)
        self.image = image
        self.rect = image.get_rect().move(position)

