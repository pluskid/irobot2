import sys
from   ConfigParser  import ConfigParser
import pygame
from   pygame.locals import *
from   pygame.sprite import Group

from   sprite   import *
from   engine   import Engine
from   event    import *

class God(object):
    def __init__(self, cfg_file):
        self._config = ConfigParser()
        self._config.read(cfg_file)
        self._robots = dict()
        self._engine = Engine(self._config)

        self._gp_robots = Group()
        self._gp_animations = Group()
        self._engine.add_group(self._gp_robots)
        self._engine.add_group(self._gp_animations)

    def add_robot(self, robot):
        robot_id = '%s.%s' % (robot['k.team'], robot['k.name'])
        self._robots[robot_id] = robot
        sprite = SpRobot(robot, self._engine.get_image('robot-2'))
        robot['k.sprite'] = sprite
        self._gp_robots.add(sprite)

        # TEST CODE
        images = self._engine.get_images('magic-small', colorkey='alpha')
        explode = SpMovingAnimation(robot, images)
        self._gp_animations.add(explode)

    def add_animation(self, animation):
        self._gp_animations.add(animation)

    def collision_detect(self, rect, obj):
        spritecollide = rect.colliderect
        def cd_group(grps):
            for grp in grps:
                for s in grp:
                    if s != obj and spritecollide(s.rect):
                        return s
            return None
        return cd_group((self._gp_robots, 
                         self._engine.map.obstacles))

    @property
    def engine(self):
        return self._engine

    def start(self):
        for robot in self._robots.itervalues():
            self.robot_born(robot)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            time_passed = self._engine.tick()
            all_dead = True
            for robot in self._robots.itervalues():
                if robot['k.alive'] == True:
                    all_dead = False
                    self.perform_action(robot, time_passed)

                if all_dead:
                    break
            self._engine.render()

    def robot_born(self, robot):
        robot.event(EvBorn())
        robot.start()
    def robot_die(self, robot):
        robot.event(EvDeath())
        
    def perform_action(self, robot, time_passed):
        action = robot['k.action']
        if action is not None:
            event = action.update(self, time_passed)
            if event is not None:
                robot['k.action'] = None
                robot.event(event)
        else:
            robot.event(EvIdle())
