from pygame.sprite import Sprite

class SpBase(Sprite):
    def __init__(self):
        Sprite.__init__(self)
    
    def damage(self, val):
        pass
