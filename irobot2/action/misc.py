from ..event import EvChangeState
from .basic  import Action

class AcChangeState(Action):
    def __init__(self, robot, state):
        Action.__init__(self, robot)
        self._state = state

    def update(self, god, intv):
        self._robot.event(EvChangeState(self._state))
        return self.event_done()

class AcNop(Action):
    """\
    Do nothing.
    """
    def update(self, god, intv):
        return self.event_done()

