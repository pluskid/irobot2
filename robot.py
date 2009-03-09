from __future__ import with_statement
from Queue      import Queue
from threading  import Thread, RLock

from event  import *
from action import *
from util   import *

class Robot(Thread):
    def __init__(self, props):
        Thread.__init__(self)
        self._queue = Queue()
        self._lock  = RLock()
        self._props = dict(props)

        self.first = True
        
    def __getitem__(self, key):
        default = None
        if isinstance(key, tuple):
            key, default = key
        with self._lock:
            return self._props.get(key, default)
    def __setitem__(self, key, val):
        with self._lock:
            self._props[key] = val

    def event(self, event):
        self._queue.put(event)

    def run(self):
        while True:
            event = self._queue.get(block=True)
            if isinstance(event, EvDeath):
                self['k.alive'] = False
                break
            elif isinstance(event, EvBorn):
                self['k.alive'] = True
            else:
                self.process_event(event)

    def process_event(self, event):
        if isinstance(event, EvIdle):
            import random
            self['k.action'] = AcMoveTo(self, vec2d(random.randint(0, 500), random.randint(0, 500)))
            # if self.first:
            #     self['k.action'] = AcTurn(self, vec2d(0, 1))
            #     self.first = False
