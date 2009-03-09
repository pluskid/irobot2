from basic import Action

class SequenceAction(Action):
    def __init__(self, robot, actions):
        Action.__init__(self, robot)
        self._actions = actions
        self._cursor = 0

    def update(self, god, intv):
        is_finish = self._actions[self._cursor].update(god, intv)
        if is_finish:
            self._cursor += 1
            if self._cursor >= len(self._actions):
                return True

