from .basic import SpBase
from ..util  import vec2d

class SpShoot(SpBase):
    def __init__(self, image, sprobot, position, 
                 direction, config, strike):
        SpBase.__init__(self)

        self._config = config
        self._strike = strike
        self.image = image
        self._sprobot = sprobot
        self.rect = self.image.get_rect()
        self._position = position
        self.rect.center = self._position
        self._direction = direction.normalized()

    def step(self, god, intv):
        self._position += self._direction*self._config['speed']*intv
        target = god.collision_detect(self.rect, (self, self._sprobot))
        if target is not None:
            self.kill()
            god.create_explosion(self._position, target, 
                                 self._config['damage']*self._strike)

    def update(self):
        self.rect.center = self._position

