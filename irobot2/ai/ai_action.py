from ..action    import AcMoveTo, AcShootAt, AcNop, AcChangeState, AcPathTo
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

class PathToAction(AIAction):
    def make_action(self, robot, dest):
        return AcPathTo(robot, dest)

class ShootAtAction(AIAction):
    valid_stypes = ('normal', 'laser', 'missile')

    def allow_action(self, robot, dest, type):
        return type in self.valid_stypes and \
                robot['k.cp'] >= self.required_cp(robot, type)

    def make_action(self, robot, dest, type):
        robot['k.cp'] -= self.required_cp(robot, type)
        return AcShootAt(robot, dest, type, robot['k.strike'])

    def required_cp(self, robot, stype):
        god = robot['k.god']
        config = god.config['setting']['shoots'][stype]
        return config['cp']

class ChangeStateAction(AIAction):
    def make_action(self, robot, state, *args):
        return AcChangeState(robot, state, *args)


all_actions = {
        'MoveTo': MoveToAction(),
        'PathTo': PathToAction(),
        'ShootAt': ShootAtAction(),
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

