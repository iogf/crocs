class Struct(list):
    pass

class Token:
    def __init__(self, value):
        self.value = value

    @classmethod
    def consume(cls, tokens):
        if isinstance(tokens[0], cls):
            return tokens[0]

    def tlen(self):
        return 1

    def clen(self):
        return len(self.value)

    def __len__(self):
        return self.clen()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))

class Eof(Token):
    pass

eof = Eof('')