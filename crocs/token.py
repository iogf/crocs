class Token:
    def __init__(self, value, start=None, end=None):
        self.value = value
        self.start = start
        self.end   = end

    def __repr__(self):
        return 'Type:%s\nValue:%s\n' % (self.__class__, self.value)