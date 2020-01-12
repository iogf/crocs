
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
    def __init__(self, value, rule=None, types=set()):
        self.value = value
        self.rule = rule if rule else self
        self.types = types

    @classmethod
    def consume(cls, tokens, exclude=[], shift=False):
        if tokens and isinstance(tokens[0], cls):
            return tokens[0]

    def plen(self):
        return 1

    def tlen(self):
        return 1

    def clen(self):
        return len(self.value)

    @classmethod
    def push_type(cls, ptree, tokens):
        pass

    def __len__(self):
        return self.clen()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))

class TokVal(Token):
    def __init__(self, value, rule=None):
        self.value = value
        self.rule = rule if rule else self
        self.types = types

    def consume(self, tokens, exclude=[], shift=False):
        if self.value == tokens[0].value:
            return tokens[0]

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
