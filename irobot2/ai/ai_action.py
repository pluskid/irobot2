from ..action    import AcMoveTo, AcShootAt, AcNop, AcChangeState
from ..exception import IllegalOperation

__all__ = ['perform_action']

class AIAction(object):
    def allow_action(self, robot, *args):
        return True
    def make_action(self, robot, *args):
        return AcNop(robot)

class MoveToAction(AIAction):
    def make_action(self, robot, dest):
        return AcMoveTo(robot, dest)

class ShootAtAction(AIAction):
    def __init__(self, stype):
        self._stype = stype

    def allow_action(self, robot, dest):
        return robot['k.cp'] >= self.required_cp(robot)

    def make_action(self, robot, dest):
        robot['k.cp'] -= self.required_cp(robot)
        return AcShootAt(robot, dest, self._stype, robot['k.strike'])

    def required_cp(self, robot):
        god = robot['k.god']
        config = god.config['setting']['shoots'][self._stype]
        return config['cp']

class ChangeStateAction(AIAction):
    def make_action(self, robot, state):
        return AcChangeState(robot, state)


all_actions = {
        'MoveTo': MoveToAction(),
        'ShootAt': ShootAtAction('normal'),
        'ChangeState': ChangeStateAction()
        }

def perform_action(name, robot, *args):
    act = all_actions.get(name)
    if act is None:
        raise IllegalOperation('No such action: %s' % name)
    if act.allow_action(robot, *args):
        robot['k.action'] = act.make_action(robot, *args)
    else:
        robot['k.action'] = AcNop(robot)

