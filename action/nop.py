from basic import Action

class AcNop(Action):
    """\
    Do nothing.
    """
    def update(self):
        return self.event_done()

