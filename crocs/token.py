
class XNode:
    def __init__(self):
        pass

class Token(XNode):
    def __init__(self, value, rule=None):
        self.value = value
        self.rule = rule if rule else self

    @classmethod
    def consume(cls, tokens, exclude=[], precedence=[]):
        if tokens and isinstance(tokens[0], cls):
            return tokens[0]

    def val(self):
        return self.value

    def tlen(self):
        return 1

    def clen(self):
        return len(self.value)

    @classmethod
    def push(cls, struct, ptree, tokens, precedence=[]):
        pass

    def __len__(self):
        return self.clen()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.value))

class TokVal(Token):
    def __init__(self, value, rule=None):
        self.value = value
        self.rule = rule if rule else self

    def consume(self, tokens, exclude=[], precedence=[]):
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
