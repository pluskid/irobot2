from   __future__ import with_statement
from   os         import path
import yaml

from   pygame.sprite import Group
from   pygame        import Rect

from   sprite import SpObject, SpDummy
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

        self._gp_shift_entrance = Group()
        self._shifts = []
        if info.has_key('shifts'):
            for shift in info['shifts']:
                sexit = shift['exit']
                sexit_objs = []
                image = resmgr.get_image(sexit['image'], basepath=img_path)
                for pos in sexit['positions']:
                    spobj = SpObject(self.tile2pixel(pos), image)
                    sexit_objs.append(spobj)
                    self._gp_all.add(spobj)
                    
                entrance = shift['entrance']
                image = resmgr.get_image(entrance['image'], basepath=img_path)
                for pos in entrance['positions']:
                    spobj = SpObject(self.tile2pixel(pos), image)
                    spobj.shift_exits = sexit_objs
                    self._gp_all.add(spobj)
                    self._gp_shift_entrance.add(spobj)


                    

        # make dummy sprites for the walls
        width  = self._geometry[0]*self._tile_size[0]
        height = self._geometry[1]*self._tile_size[1]
        walls = [SpDummy(Rect(-1, 0, 1, height)),
                 SpDummy(Rect(0, -1, width, 1)),
                 SpDummy(Rect(width, 0, 1, height)),
                 SpDummy(Rect(0, height, width, 1))]
        for wall in walls:
            self._gp_obstacle.add(wall)

    @property
    def obstacles(self):
        return self._gp_obstacle

    def render(self, screen):
        screen.blit(self._background, self._background.get_rect())
        self._gp_all.draw(screen)

    def tile2pixel(self, pos):
        x = pos[0]*self._tile_size[0]
        y = pos[1]*self._tile_size[1]
        return vec2d(x, y)

