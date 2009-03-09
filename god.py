import sys
from   ConfigParser  import ConfigParser
import pygame
from   pygame.locals import *
from   pygame.sprite import Group

import resource
from   sprite   import *
from   engine   import Engine
from   event    import *

class God(object):
    def __init__(self, cfg_file):
        self._config = ConfigParser()
        self._config.read(cfg_file)
        self._robots = dict()
        self._resmgr = resource.ResourceManager()
        self._engine = Engine(self._config)

        self._gp_robots = Group()
        self._engine.add_group(self._gp_robots)

    def add_robot(self, robot):
        robot_id = '%s.%s' % (robot['k.team'], robot['k.name'])
        self._robots[robot_id] = robot
        sprite = SpRobot(robot, self._resmgr.get_image('tank'))
        robot['k.sprite'] = sprite
        self._gp_robots.add(sprite)

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
            is_done = action.update(self, time_passed)
            if is_done:
                robot['k.action'] = None
                robot.event(EvDone())
        else:
            robot.event(EvIdle())
