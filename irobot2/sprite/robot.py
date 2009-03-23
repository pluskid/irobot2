import pygame

from .basic  import SpBase
from ..util  import vec2d
from ..event import EvHurt

class SpRobot(SpBase):
    def __init__(self, robot, image):
        SpBase.__init__(self)
        self._robot = robot
        self._base_image = image
        self._bound_rect = pygame.Rect(image.get_rect())
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
        self.rect.center = (pos[0], pos[1])

    @property
    def bound_rect(self):
        return self._bound_rect

    def rotate_image(self):
        self._direction = self._robot['k.direction']
        self.image = pygame.transform.rotate(
                self._base_image, -self._direction.angle)
    def alpha_image(self):
        self._alpha = self._robot['k.alpha']
        self.image.set_alpha(self._alpha)

    def hurt(self, damage, god, source):
        robot = self._robot
        damage -= damage*robot['k.defend']
        robot['k.hp'] -= damage
        if robot['k.hp'] <= 0:
            self.die(god)
            god.robot_die(self._robot)
        else:
            if damage > 0:
                robot.event(EvHurt(damage, source))
