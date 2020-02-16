class XNode:
    def __init__(self):
        pass

class PTree(list):
    """
    """
    __slots__ = ['rule', 'type', 'result']

    def __init__(self, iterable=(), rule=None, type=None):
        super(PTree, self).__init__(iterable)

        self.rule = rule
        self.type = type
        self.result = None

    def eval(self, handle):
        if handle:
            self.result = handle(*self)

    def val(self):
        return self.result

class Token(XNode):
    def __init__(self, data, cast=None):
        self.data = data
        self.value = cast(data) if cast else data
        self.type = self.__class__

    @classmethod
    def validate(cls, tokens):
        tok = tokens.get()
        return tok != None and cls.istype(tok)

    @classmethod
    def istype(cls, tok):
        return tok.type is cls

    def val(self):
        return self.value
    
    def tlen(self):
        return 1

    def clen(self):
        return len(self.data)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.data))

class TokVal(Token):
    def __init__(self, value):
        self.value = value

    def validate(self, tokens):
        tok = tokens.get()
        return tok != None and self.istype(tok)

    def istype(self, tok):
        return self.value == tok.value

class Eof(Token):
    pass

class Sof(Token):
    pass

class TSeq(list):
    """
    This is meant to be returned by XNode's instances
    that extract strings from a given doc sequentially.
    """

    def __init__(self, *args):
        self.extend(args)

    def clen(self):
        count = 0
        for ind in self:
            count += ind.clen()
        return count

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

