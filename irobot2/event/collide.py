from basic import Event

class EvCollide(Event):
    name = 'collide'

    def __init__(self, target):
        Event.__init__(self)
        self.target = target


