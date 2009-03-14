from vec2d import vec2d
from queue import PriorityQueue

class DictObj(dict):
    def __init__(self, *args):
        dict.__init__(self, *args)
        self.__dict__ = self


