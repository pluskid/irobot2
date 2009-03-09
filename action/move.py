from basic   import Action
from compose import SequenceAction
from util    import *

__all__ = ['AcMove', 'AcTurn', 'AcMoveTo']

class AcMove(Action):
    def __init__(self, robot, dest):
        Action.__init__(self, robot)
        self._dest = dest

    def update(self, god, intv):
        vdist = (self._dest-self._robot['k.position'])
        distance = intv*self._robot['k.speed']
        if distance >= vdist.length:
            self._robot['k.position'] = self._dest
            return True
        self._robot['k.position'] += vdist.normalized()*distance
        return False

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
            self._robot['k.direction'] = direction.rotated(ang_remain)
            return True
        self._robot['k.direction'] = direction.rotated(ang)
        return False

class AcMoveTo(Action):
    def __init__(self, robot, dest):
        Action.__init__(self, robot)
        aturn = AcTurn(robot, dest-robot['k.position'])
        amove = AcMove(robot, dest)
        self._action = SequenceAction(robot, [aturn, amove])

    def update(self, god, intv):
        return self._action.update(god, intv)
