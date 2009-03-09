class Action(object):
    """\
    Base class for all actions. Real actions should
    implement update(god, intv) method to do action updating.
    """
    def __init__(self, robot):
        self._robot = robot
        
    def finish(self):
        self._robot['k.action'] = None
