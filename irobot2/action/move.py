from __future__ import with_statement

import pygame

from .basic   import Action
from .compose import SequenceAction
from ..util   import vec2d
from ..sprite import SpAnimation
from ..event  import EvCollide

__all__ = ['AcMove', 'AcTurn', 'AcMoveTo', 'AcAppear', 
           'AcDisappear', 'AcShift']

class AcMove(Action):
    def __init__(self, robot, dest):
        Action.__init__(self, robot)
        self._dest = dest

    def update(self, god, intv):
        vdist = (self._dest-self._robot.position)
        distance = intv*self._robot['k.speed']
        if distance >= vdist.length:
            new_pos = self._dest
        else:
            new_pos = self._robot.position+vdist.normalized()*distance

        rect = pygame.Rect(self._robot['k.sprite'].bound_rect)
        rect.center = new_pos
        target = god.collision_detect(rect, (self._robot['k.sprite'],))
        if target is not None:
            return EvCollide(target)

        self._robot.position = new_pos
        if new_pos == self._dest:
            return self.event_done()
        return None

class AcTurn(Action):
    def __init__(self, robot, direction):
        Action.__init__(self, robot)
        self._direction = direction

    def update(self, god, intv):
        direction = self._robot['k.direction']
        ang = self._robot['k.angle_speed']*intv
        ang_remain = direction.get_angle_between(self._direction)
        if ang_remain < 0:
            ang = -ang
        if abs(ang) >= abs(ang_remain):
            final_direction = direction.rotated(ang_remain)
        else:
            final_direction = direction.rotated(ang)

        self._robot['k.direction'] = final_direction
        if abs(ang) >= abs(ang_remain):
            return self.event_done()
        return None

class AcMoveTo(SequenceAction):
    def __init__(self, robot, dest):
        Action.__init__(self, robot)
        aturn = AcTurn(robot, dest-robot.position)
        amove = AcMove(robot, dest)
        SequenceAction.__init__(self, robot, [aturn, amove])

class AcDisappear(Action):
    def __init__(self, robot):
        Action.__init__(self, robot)
        self._animation = None
        self._alpha_dec = 255

    def update(self, god, intv):
        if self._animation is None:
            images = god.engine.get_images('magic-small', colorkey='alpha')
            self._animation = SpAnimation(self._robot.position, images)
            god.add_animation(self._animation)
            self._alpha_dec = self._robot['k.alpha']/len(images)+1
        else:
            alpha = max(0, self._robot['k.alpha']-self._alpha_dec)
            self._robot['k.alpha'] = alpha

        if self._animation.alive():
            return None
        else:
            return self.event_done()

class AcAppear(Action):
    def __init__(self, robot):
        Action.__init__(self, robot)
        self._animation = None
        self._alpha_inc = 255

    def update(self, god, intv):
        if self._animation is None:
            images = god.engine.get_images('magic-small', colorkey='alpha')
            self._animation = SpAnimation(self._robot.position, images)
            god.add_animation(self._animation)
            self._alpha_inc = (255-self._robot['k.alpha'])/len(images)+1
        else:
            alpha = min(255, self._robot['k.alpha']+self._alpha_inc)
            self._robot['k.alpha'] = alpha

        if self._animation.alive():
            return None
        else:
            return self.event_done()

class AcShift(Action):
    class DirectMove(Action):
        def __init__(self, robot, dest):
            Action.__init__(self, robot)
            self._dest = dest
        def update(self, god, intv):
            self._robot.position = self._dest
            return self.event_done()

    def __init__(self, robot, dest):
        Action.__init__(self, robot)
        adisappear = AcDisappear(robot)
        amove = AcShift.DirectMove(robot, dest)
        aappear = AcAppear(robot)

        self._action = SequenceAction(robot, 
                                      [adisappear, amove, aappear])

    def update(self, god, intv):
        return self._action.update(god, intv)
