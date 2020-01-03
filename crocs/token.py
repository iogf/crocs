class XNode:
    def __init__(self):
        self.children = []

    def register(self, xnode):
        self.children.append(xnode)
    pass

    @classmethod
    def is_refer(self):
        return False

class Token(XNode):
    def __init__(self, value):
        self.value = value

    @classmethod
    def consume(cls, tokens, exclude=[]):
        if tokens and isinstance(tokens[0], cls):
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