from   __future__ import with_statement
from   os         import path
import yaml

from   pygame.sprite import Group

from   sprite import SpObject
from   util   import vec2d

class GameMap(object):
    def __init__(self, resmgr, map_path=None):
        if map_path is None:
            map_path = path.join(path.dirname(__file__), 
                                 'resource', 'map', 'default')
        self._background = resmgr.get_image('map', basepath=map_path)
        with open(path.join(map_path, 'map.yml')) as ins:
            info = yaml.load(ins.read())
        self._tile_size = info['info']['tile_size']
        self._geometry = info['info']['geometry']

        self._gp_all = Group()
        self._gp_obstacle = Group()
        img_path = path.join(map_path, 'image')
        for obj in info['objects']:
            image = resmgr.get_image(obj['image'], basepath=img_path)
            for pos in obj['positions']:
                spobj = SpObject(self.tile2pixel(pos), image)
                self._gp_all.add(spobj)
                if obj['type'] in ['obstacle', 'box']:
                    self._gp_obstacle.add(spobj)

    def render(self, screen):
        screen.blit(self._background, self._background.get_rect())
        self._gp_all.draw(screen)

    def tile2pixel(self, pos):
        x = pos[0]*self._tile_size[0]
        y = pos[1]*self._tile_size[1]
        return vec2d(x, y)

