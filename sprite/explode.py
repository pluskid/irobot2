import pygame
from   pygame.sprite import Sprite

from util import vec2d

class SpExplode(Sprite):
    def __init__(self, position, images):
        Sprite.__init__(self)
        self._position = position
        self._images = images
        self._cursor = -1
        self._counter = 0

    def update(self):
        if self._counter == 0:
            self._counter = 2
            self._cursor += 1
            if self._cursor >= len(self._images):
                self.kill()
            else:
                self.image = self._images[self._cursor]
                self.rect = self.image.get_rect()
                self.rect.center = (self._position[0], self._position[1])
        self._counter -= 1

