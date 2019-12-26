class Token:
    def __init__(self, value):
        self.value = value

    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))

class Eof(Token):
    pass

eof = Eof('')