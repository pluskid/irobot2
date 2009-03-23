from ..event import EvChangeState
from .basic  import Action

class AcChangeState(Action):
    def __init__(self, robot, state, *args):
        Action.__init__(self, robot)
        self._state = state
        self._args = args

    def update(self, god, intv):
        self._robot.event(EvChangeState(self._state, *self._args))
        return self.event_done()

class AcNop(Action):
    """\
    Do nothing.
    """
    def update(self, god, intv):
        return self.event_done()

