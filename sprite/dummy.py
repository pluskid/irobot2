from pygame.sprite import Sprite

class SpDummy(Sprite):
    def __init__(self, rect):
        Sprite.__init__(self)
        self.rect = rect

    def draw(self):
        pass
