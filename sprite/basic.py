from pygame.sprite import Sprite

from util import vec2d

class SpBase(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.hp = float('inf')
    
    def hurt(self, damage, god):
        orig_hp = self.hp
        self.hp -= damage
        if self.hp <= 0:
            god.create_explosion_animation(vec2d(self.rect.center),
                                           'explode-large')
            self.kill()
        if self.hp < orig_hp:
            pass #TODO: add effect here

