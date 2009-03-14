class Event(object):
    "Base class for all events"
    PRIORITY_NORMAL    = 2
    PRIORITY_IMPORTANT = 1
    PRIORITY_CRITICAL  = 0

    name = 'k.event'
    priority = PRIORITY_NORMAL

    def __cmp__(self, other):
        if self.priority < other.priority:
            return -1
        elif self.priority == other.priority:
            return 0
        return 1


class EvDeath(Event):
    "Event for a robot death"
    name = 'k.death'
    priority = Event.PRIORITY_CRITICAL

class EvBorn(Event):
    "Event for a robot born"
    name = 'k.born'

class EvDone(Event):
    "Event for action done"
    name = 'k.done'

class EvIdle(Event):
    "Event for idle robot"
    name = 'idle'

class EvChangeState(Event):
    "Event for state changing"
    name = 'k.change_state'
    priority = Event.PRIORITY_IMPORTANT

    def __init__(self, state):
        Event.__init__(self)
        self.state = state
