class State(object):
    def initialize(self):
        pass
    def loop(self, run_action):
        pass
    def terminate(self):
        pass

    def handle_event(self, event_name, *args):
        handle_name = 'on_%s' % event_name
        if hasattr(self, handle_name):
            getattr(self, handle_name)(*args)
