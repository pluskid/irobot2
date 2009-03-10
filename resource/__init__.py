import os
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
            image = self.load_image(fn, colorkey)
            self._res[realkey] = image
        return image

    def get_images(self, key, colorkey=-1):
        realkey = 'images.%s' % key
        images = self._res.get(realkey)
        if images is None:
            img_dir = path.join(path.dirname(__file__), 'image', key)
            fns = os.listdir(img_dir)
            fns.sort()
            images = [self.load_image(path.join(img_dir, fn), colorkey) 
                    for fn in fns]
            self._res[realkey] = images
        return images

    def load_image(self, fn, colorkey):
        image = pygame.image.load(fn)
        if colorkey == 'alpha':
            image = image.convert_alpha()
        else:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            if colorkey is not None:
                image.set_colorkey(colorkey, RLEACCEL)
        return image
