from ..util      import DictObj
from ..exception import IRobotError
from .basic      import Event

class EvHurt(Event):
    name = 'hurt'

    def __init__(self, damage, source):
        self.damage = damage

        src_type = type(source).__name__
        if src_type == 'SpShoot':
            self.source = DictObj({
                'type': 'shoot',
                'shoot_type': source.stype,
                'direction': source.direction,
                'speed': source.speed
            })
        else:
            raise IRobotError('Unknown hurt source: %s' % source)

