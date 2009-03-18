from vec2d import vec2d
from queue import PriorityQueue

class DictObj(dict):
    def __init__(self, *args):
        dict.__init__(self, *args)
        self.__dict__ = self

def make_2darray(elem, geometry):
    return [[elem for i in range(geometry[1])]
            for j in range(geometry[0])]
