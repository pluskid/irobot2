from basic import Action

class SequenceAction(Action):
    class FinishNormal(object):
        pass

    def __init__(self, robot, actions):
        Action.__init__(self, robot)
        self._actions = actions
        self._cursor = 0

        for ac in self._actions:
            ac.event_done = SequenceAction.FinishNormal

    def update(self, god, intv):
        event = self._actions[self._cursor].update(god, intv)
        if isinstance(event, SequenceAction.FinishNormal):
            self._cursor += 1
            if self._cursor >= len(self._actions):
                return self.event_done()
        else:
            # None or special event that term action abnormally
            return event

