class Event(object):
    "Base class for all events"
    name = 'k.event'

class EvDeath(Event):
    "Event for a robot death"
    name = 'k.death'

class EvBorn(Event):
    "Event for a robot born"
    name = 'k.born'

class EvDone(Event):
    "Event for action done"
    name = 'k.done'

class EvIdle(Event):
    "Event for idle robot"
    name = 'idle'

