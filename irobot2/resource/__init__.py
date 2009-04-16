import os
from   os import path

import pygame
from   pygame.locals import *
from   pygame.mixer  import Sound

class ResourceManager(object):
    def __init__(self):
        self._res = dict()

    def get_sound(self, key, basepath=None):
        if basepath is None:
            basepath = path.join(path.dirname(__file__), 'sound')
        realkey = 'sound.%s.%s' % (basepath, key)
        sound = self._res.get(realkey)
        if sound is None:
            fn = path.join(basepath, '%s.wav' % key)
            sound = Sound(fn)
            self._res[realkey] = sound
        return sound

    def get_image(self, key, colorkey='alpha', basepath=None):
        if basepath is None:
            basepath = path.join(path.dirname(__file__), 'image')
        realkey = 'image.%s.%s' % (basepath, key)
        image = self._res.get(realkey)
        if image is None:
            fn = path.join(basepath, '%s.png' % key)
            image = self.load_image(fn, colorkey)
            self._res[realkey] = image
        return image

    def get_images(self, key, colorkey='alpha', basepath=None):
        if basepath is None:
            basepath = path.join(path.dirname(__file__), 'image')
        realkey = 'images.%s.%s' % (basepath, key)
        images = self._res.get(realkey)
        if images is None:
            img_dir = path.join(basepath, key)
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
