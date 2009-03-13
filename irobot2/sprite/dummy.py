from .basic import SpBase

class SpDummy(SpBase):
    """Only rect property for collision detection,
    no image property so that nothing will show on
    screen.
    """
    def __init__(self, rect):
        SpBase.__init__(self)
        self.rect = rect
