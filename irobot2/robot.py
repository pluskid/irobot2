from __future__ import with_statement
from threading  import Thread, RLock

from pygame     import Rect

from .util      import PriorityQueue

class Robot(Thread):
    public_props = ['type', 'team', 'name', 'direction', 'position',
                    'speed', 'angle_speed', 'strike', 'defend', 'sight',
                    'hp', 'cp']

    def __init__(self, props):
        Thread.__init__(self)
        self._queue = PriorityQueue()
        self._lock  = RLock()
        self._props = dict(props)
        self._ai = None
        self._overlays = []

    def add_overlay(self, overlay):
        self._overlays.append(overlay)

    def born(self):
        self['k.alive'] = True

    def die(self):
        self['k.alive'] = False
        for overlay in self._overlays:
            overlay.kill()
        
    def __getitem__(self, key):
        default = None
        if isinstance(key, tuple):
            key, default = key
        with self._lock:
            return self._props.get(key, default)
    def __setitem__(self, key, val):
        with self._lock:
            self._props[key] = val

    @property
    def eyesight_rect(self):
        return Rect(0, 0, self['k.sight'], self['k.sight'])

    def event(self, event):
        self._queue.put(event)

    def assign_ai(self, ai):
        self._ai = ai

    def run(self):
        while True:
            event = self._queue.get(block=True)
            self._ai.process_event(event)

