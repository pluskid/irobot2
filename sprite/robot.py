import pygame
from   pygame.sprite import Sprite

from util import vec2d

class SpRobot(Sprite):
    def __init__(self, robot, image):
        Sprite.__init__(self)
        self._robot = robot
        self._base_image = image
        self.rotate_image()
        self.alpha_image()

    def update(self):
        props = ['direction', 'alpha']
        for prop in props:
            val = self._robot['k.%s' % prop]
            if val != getattr(self, '_%s' % prop):
                self.rotate_image()
                self.alpha_image()
                break

        pos = self._robot['k.position']
        self.rect = self.image.get_rect()
        self.rect.center = (pos.x, pos.y)

    def rotate_image(self):
        self._direction = self._robot['k.direction']
        self.image = pygame.transform.rotate(
                self._base_image, -self._direction.angle)
    def alpha_image(self):
        self._alpha = self._robot['k.alpha']
        self.image.set_alpha(self._alpha)
        pygame.draw.rect(self.image, (255, 0, 0), self.image.get_rect(), 1)
