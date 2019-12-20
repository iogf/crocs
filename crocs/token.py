class Token:
    def __init__(self, value, start=None, end=None):
        self.value = value
        self.start = start
        self.end   = end

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))