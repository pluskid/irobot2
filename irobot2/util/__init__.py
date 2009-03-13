from vec2d import vec2d

class DictObj(dict):
    def __init__(self, *args):
        dict.__init__(self, *args)
        self.__dict__ = self


