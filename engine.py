import pygame
from   pygame.locals import *

from resource import ResourceManager

class Engine(object):
    def __init__(self, config):
        self._resmgr = ResourceManager()
        self._fps = config.getint('engine', 'fps')
        self._width = config.getint('engine', 'width')
        self._height = config.getint('engine', 'height')
        fullscreen = False
        if config.has_option('engine', 'fullscreen'):
            if config.get('engine', 'fullscreen') in ('True', 'true', '1'):
                fullscreen = True
        if fullscreen:
            flag = DOUBLEBUF | FULLSCREEN | HWSURFACE
        else:
            flag = DOUBLEBUF

        pygame.init()
        self._screen = pygame.display.set_mode(
                (self._width, self._height), flag)
        self._clock = pygame.time.Clock()

        self._groups = []

    def get_image(self, key, colorkey=-1):
        return self._resmgr.get_image(key, colorkey=colorkey)
    def get_images(self, key, colorkey=-1):
        return self._resmgr.get_images(key, colorkey=colorkey)

    def tick(self):
        return self._clock.tick(self._fps)

    def add_group(self, group):
        self._groups.append(group)

    def render(self):
        # draw backgrounds
        bg = self._resmgr.get_image('background', colorkey=None)
        bg_rect = bg.get_rect()
        nrows = int(self._screen.get_height() / bg_rect.height)+1
        ncols = int(self._screen.get_width() / bg_rect.width)+1
        for y in range(nrows):
            for x in range(ncols):
                bg_rect.topleft = (x*bg_rect.width, y*bg_rect.height)
                self._screen.blit(bg, bg_rect)

        for grp in self._groups:
            grp.update()
            grp.draw(self._screen)

        pygame.display.flip()
