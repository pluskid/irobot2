from __future__ import with_statement
from Queue      import Queue
from threading  import Thread, RLock

class Robot(Thread):
    def __init__(self, props):
        Thread.__init__(self)
        self._queue = Queue()
        self._lock  = RLock()
        self._props = dict(props)
        self._ai = None
        
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

    def assign_ai(self, ai):
        self._ai = ai

    def run(self):
        while True:
            event = self._queue.get(block=True)
            self._ai.process_event(event)

