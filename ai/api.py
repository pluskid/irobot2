class State(object):
    def initialize(self):
        pass
    def loop(self, run_action):
        pass
    def terminate(self):
        pass

    def handle_event(self, event):
        handle_name = 'on_%s' % event.name
        if hasattr(self, handle_name):
            return getattr(self, handle_name)(event)
