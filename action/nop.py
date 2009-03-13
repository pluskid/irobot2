from basic import Action

class AcNop(Action):
    """\
    Do nothing.
    """
    def update(self, god, intv):
        return self.event_done()

