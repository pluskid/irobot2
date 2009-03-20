import pygame

from .dummy     import SpDummy
from .robot     import SpRobot
from .shoot     import SpShoot
from .basic     import SpBase
from .animation import SpAnimation, SpMovingAnimation
from .overlay   import SpHPOverlay
from ..util     import vec2d


class SpObject(SpBase):
    def __init__(self, position, image):
        SpBase.__init__(self)
        self.image = image
        self.rect = image.get_rect().move(position)

