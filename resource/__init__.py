from   os import path

import pygame
from   pygame.locals import *

class ResourceManager(object):
    def __init__(self):
        self._res = dict()

    def get_image(self, key, colorkey=-1):
        realkey = 'image.%s' % key
        image = self._res.get(realkey)
        if image is None:
            fn = path.join(path.dirname(__file__), 'image',
                    '%s.png' % key)
            image = pygame.image.load(fn).convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            if colorkey is not None:
                image.set_colorkey(colorkey, RLEACCEL)
            self._res[realkey] = image
        return image
