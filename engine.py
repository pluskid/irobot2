import pygame
from   pygame.locals import *

class Engine(object):
    def __init__(self, config):
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

    def tick(self):
        return self._clock.tick(self._fps)

    def add_group(self, group):
        self._groups.append(group)

    def render(self):
        # draw backgrounds
        self._screen.fill((0, 0, 0))

        for grp in self._groups:
            grp.update()
            grp.draw(self._screen)

        pygame.display.flip()
