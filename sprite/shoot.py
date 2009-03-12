from pygame.sprite import Sprite

from util import vec2d

class SpShoot(Sprite):
    def __init__(self, image, sprobot, position, direction, speed):
        Sprite.__init__(self)
        self.image = image
        self._sprobot = sprobot
        self.rect = self.image.get_rect()
        self._position = position
        self.rect.center = self._position
        self._direction = direction.normalized()
        self._speed = speed

    def step(self, god, intv):
        self._position += self._direction*self._speed*intv
        target = god.collision_detect(self.rect, (self, self._sprobot))
        if target is not None:
            self.kill()
            god.create_explosion(self._position)

    def update(self):
        self.rect.center = self._position

