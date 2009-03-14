from ..util import vec2d
from .basic import SpBase

class SpAnimation(SpBase):
    def __init__(self, position, images, delay=1):
        SpBase.__init__(self)
        self._position = position
        self._images = images
        self._cursor = -1
        self._counter = 0
        self._counter_bound = delay

    def update(self):
        if self._counter == 0:
            self._counter = self._counter_bound
            self._cursor += 1
            if self._cursor >= len(self._images):
                self.kill()
            else:
                self.image = self._images[self._cursor]
                self.rect = self.image.get_rect()
                self.rect.center = (self._position[0], self._position[1])
        self._counter -= 1


class SpMovingAnimation(SpAnimation):
    def __init__(self, robot, images, delay=1):
        SpAnimation.__init__(self, robot['k.position'], 
                             images, delay=delay)
        self._robot = robot

    def update(self):
        self._position = self._robot['k.position']
        SpAnimation.update(self)

