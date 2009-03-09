import pygame
from   pygame.sprite import Sprite

from util import vec2d

class SpRobot(Sprite):
    def __init__(self, robot, image):
        Sprite.__init__(self)
        self._robot = robot
        self._base_image = image
        self.rotate_image()

    def update(self):
        direction = self._robot['k.direction']
        if direction != self._direction:
            self.rotate_image()
        pos = self._robot['k.position']
        self.rect = self.image.get_rect()
        self.rect.center = (pos.x, pos.y)

    def rotate_image(self):
        self._direction = self._robot['k.direction']
        self.image = pygame.transform.rotate(
                self._base_image, -self._direction.angle)



