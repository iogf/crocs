class XNode:
    def __init__(self):
        pass

class PTree(list):
    """
    """
    __slots__ = ['rule', 'type', 'result', 'data']

    def __init__(self, iterable=(), rule=None, type=None):
        super(PTree, self).__init__(iterable)

        self.rule = rule
        self.type = type
        self.data = type
        self.result = None

    def eval(self, handle):
        if handle:
            self.result = handle(*self)

    def val(self):
        return self.result

# class Token(namedtuple('Token', ('data', 'type', 'value'))):
    # def val(self):
        # return self.value
    # 
    # def tlen(self):
        # return 1
# 
    # def clen(self):
        # return len(self.data)
# 
    # def __repr__(self):
        # return '%s(%s)' % (self.type.__name__, repr(self.data))

class Token:
    __slots__=['data', 'offset', 'type', 'value']

    def __init__(self, data, type=None, cast=None, offset=0):
        self.data = data
        self.value = cast(data) if cast else data
        self.type = type
        self.offset = offset

    def val(self):
        return self.value
    
    def tlen(self):
        return 1

    def clen(self):
        return len(self.data)

    def __repr__(self):
        return '%s(%s)' % (self.type.__name__, repr(self.data))

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

class TokType:
    @classmethod
    def istype(cls, tok):
        return tok.type is cls

class TokVal:
    def __init__(self, data):
        self.data = data
        self.type = TokVal

    def istype(self, tok):
        return self.data == tok.data

    def __repr__(self):
        return 'TokVal(%s)' % repr(self.data)

class Eof(TokType):
    pass

class Sof(TokType):
    pass

class Num(TokType):
    pass

class Plus(TokType):
    pass

class Minus(TokType):
    pass

class Div(TokType):
    pass

class Mul(TokType):
    pass

class RP(TokType):
    pass

class LP(TokType):
    pass

class Blank(TokType):
    pass

class Keyword(TokType):
    pass

class Identifier(TokType):
    pass

class Colon(TokType):
    pass

class DoubleQuote(TokType):
    pass

class Quote(TokType):
    pass

class Comma(TokType):
    pass

class LB(TokType):
    pass

class RB(TokType):
    pass

class Word(TokType):
    pass

