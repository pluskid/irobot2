from action    import *
from exception import IllegalOperation

__all__ = ['perform_action']

class AIAction(object):
    def allow_action(self, robot, *args):
        return True
    def make_action(self, robot, *args):
        return AcNop(robot)

class MoveToAction(AIAction):
    def make_action(self, robot, dest):
        return AcMoveTo(robot, dest)

class ShootAction(AIAction):
    def __init__(self, stype):
        self._stype = stype

    def allow_action(self, robot):
        god = robot['k.god']
        config = god.config['setting']['shoots'][self._stype]
        return robot['k.cp'] >= config['cp']

    def make_action(self, robot):
        # TODO: consider strike of robot
        return AcShoot(robot, self._stype)

all_actions = {
        'MoveTo': MoveToAction(),
        'Shoot': ShootAction('normal')
        }

def perform_action(name, robot, *args):
    act = all_actions.get(name)
    if act is None:
        raise IllegalOperation('No such action: %s' % name)
    if act.allow_action(robot, *args):
        robot['k.action'] = act.make_action(robot, *args)
    else:
        robot['k.action'] = AcNop(robot)

