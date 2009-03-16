from ..robot import Robot

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

class Descriptor(object):
    def __init__(self, name):
        self._name = name
        self._meth_name = 'get_%s'%name
    def __get__(self, instance, owner):
        return getattr(instance, self._meth_name)()
    def __set__(self, instance, value):
        raise AttributeError('attribute %s is read only' % self._name)
    def __delete__(self, instance):
        raise AttributeError('attribute %s is read only' % self._name)

for prop in Robot.public_props:
    setattr(State, prop, Descriptor(prop))

