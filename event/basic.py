class Event(object):
    "Base class for all events"
    pass

class EvDeath(Event):
    "Event for a robot death"
    pass

class EvBorn(Event):
    "Event for a robot born"
    pass

class EvIdle(Event):
    "Event for idle robot"
    pass

