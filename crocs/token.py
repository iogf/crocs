
class XNode:
    def __init__(self):
        pass

class TSeq(list):
    """
    This is meant to be returned by XNode's instances
    that extract strings from a given doc sequentially.
    """

    def __init__(self, *args):
        self.extend(args)
        self.slen = 0

    def clen(self):
        val = map(len, self)
        return sum(val)

    def __len__(self):
        return self.clen()

class PTree(list):
    """
    """

    def __init__(self, rule, *args):
        self.rule = rule
        self.result = None
        self.count = 0

        for ind in args:
            self.append(ind)

    def append(self, ptree):
        super(PTree, self).append(ptree)
        self.count = self.count + ptree.tlen()

    def eval(self, handles):
        result = self
        for ind in handles:
            result = ind(*result)

        if result is not self:
            self.result = result 

    def val(self):
        return self.result

    def tlen(self):
        return self.count

class Token(XNode):
    def __init__(self, value, rule=None):
        self.value = value
        self.rule = rule if rule else self

    @classmethod
    def consume(cls, tokens, exclude=[], precedence=[]):
        if tokens and isinstance(tokens[0], cls):
            return PTree(cls, tokens[0])

    def val(self):
        return self.value

    def tlen(self):
        return 1

    def clen(self):
        return len(self.value)

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
