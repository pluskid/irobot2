import pygame
from   pygame.locals import *

from resource import ResourceManager
from game_map import GameMap

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

        if config.has_option('game', 'map'):
            self._map = GameMap(self._resmgr, config.get('game', 'map'))
        else:
            self._map = GameMap(self._resmgr)

        self._groups = []

    def get_image(self, key, colorkey='alpha', basepath=None):
        return self._resmgr.get_image(key, colorkey=colorkey,
                                     basepath=basepath)
    def get_images(self, key, colorkey='alpha', basepath=None):
        return self._resmgr.get_images(key, colorkey=colorkey,
                                      basepath=basepath)

    @property
    def map(self):
        return self._map

    def tick(self):
        return self._clock.tick(self._fps)

    def add_group(self, group):
        self._groups.append(group)

    def render(self):
        self._map.render(self._screen)

        for grp in self._groups:
            grp.update()
            grp.draw(self._screen)

        pygame.display.flip()
