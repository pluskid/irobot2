from pygame import Surface, draw, Rect

from .basic import SpBase
from ..util import vec2d

class SpOverlay(SpBase):
    def __init__(self, robot):
        """\
        Base class of overlay. Subclass should
        init the following attributes in the constructor:

         - self.image
         - self.rect
         - self.offset

        and the `do_update` method should be defined to
        do updating.
        """
        SpBase.__init__(self)
        self._robot = robot

    def update(self):
        self.rect.center = self._robot['k.position']+self.offset
        self.do_update()
        self.image.set_alpha(self._robot['k.alpha'])

class SpHPOverlay(SpOverlay):
    def __init__(self, robot):
        SpOverlay.__init__(self, robot)
        sprect = robot['k.sprite'].image.get_rect()
        dist = max(sprect.width, sprect.height)/2
        self.offset = vec2d(0, -dist-5)
        cfg = robot['k.god'].config['setting']['overlays']['hp']
        size = cfg['size']
        self.image = Surface(size)
        self.rect = self.image.get_rect()
        self.border_color = cfg['border_color']
        self.fill_color   = cfg['fill_color']
        self.bg_color     = cfg['bg_color']
        self.hp_tot = robot['k.god'].prototype(robot['k.type'])['hp']

    def do_update(self):
        hp = self._robot['k.hp']
        width = int(self.rect.width*hp/self.hp_tot)
        self.image.fill(self.bg_color)
        draw.rect(self.image, self.fill_color,
                  Rect(0, 0, width, self.rect.height))
        draw.rect(self.image, self.border_color,
                  Rect(0, 0, self.rect.width, self.rect.height), 1)
