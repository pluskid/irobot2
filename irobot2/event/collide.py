from ..util      import DictObj
from ..exception import IRobotError
from .basic      import Event

class EvCollide(Event):
    name = 'collide'

    def __init__(self, target):
        Event.__init__(self)
        target_type = type(target).__name__
        if target_type == 'SpRobot':
            robot = target._robot
            self.target = DictObj({
                'type': 'robot',
                'team': robot['k.team'],
                'name': robot['k.name']
            })
        elif target_type == 'SpObject':
            if target.type in ['box', 'treasure']:
                self.target = DictObj({
                    'type': target.type,
                    'hp': target.hp,
                    'position': target.position
                })
            elif target.type == 'obstacle':
                self.target = DictObj({'type': 'obstacle'})
            else:
                raise IRobotError('Unknown collide target: %s' % target)
        elif target_type == 'SpDummy':
            self.target = DictObj({'type': 'obstacle'})
        else:
            raise IRobotError('Unknown collide target: %s' % target)

