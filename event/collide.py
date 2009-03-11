from basic import Event

class EvCollide(Event):
    def __init__(self, target):
        Event.__init__(self)
        self.target = target


