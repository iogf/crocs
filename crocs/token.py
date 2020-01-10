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
    def __init__(self, value, rule=None, type=None):
        self.value = value
        self.rule = rule if rule else self
        self.type = type

    @classmethod
    def consume(cls, tokens, exclude=[]):
        if tokens and isinstance(tokens[0], cls):
            return tokens[0]

    def plen(self):
        return 1

    def tlen(self):
        return 1

    def clen(self):
        return len(self.value)

    def __len__(self):
        return self.clen()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))

class Num(Token):
    pass

class Plus(Token):
    pass

class Minus(Token):
    pass

class Div(Token):
    pass

class Mul(Token):
    pass

class RP(Token):
    pass

class LP(Token):
    pass

class Blank(Token):
    pass

class Eof(Token):
    pass

eof = Eof('')