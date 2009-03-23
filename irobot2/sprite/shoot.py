import pygame

from .basic import SpBase
from ..util  import vec2d

class SpShoot(SpBase):
    def __init__(self, image, sprobot, position, 
                 direction, config, strike):
        SpBase.__init__(self)

        self._config = config
        self._strike = strike
        self._direction = direction.normalized()
        self.image = pygame.transform.rotate(image, -self._direction.angle)
        self._sprobot = sprobot
        self.rect = self.image.get_rect()
        self._position = position
        self.rect.center = self._position

    def step(self, god, intv):
        self._position += self._direction*self._config['speed']*intv
        target = god.collision_detect(self.rect, (self, self._sprobot))
        if target is not None:
            self.kill()
            god.create_explosion(self._position, target, 
                                 self._config['damage']*self._strike,
                                 self)

    @property
    def direction(self):
        return self._direction
    @property
    def speed(self):
        return self._config['speed']

    def update(self):
        self.rect.center = self._position

