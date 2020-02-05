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
        self.index = 0

    def reset(self):
        self.index = 0

    def shift(self):
        self.index = self.index + 1

    def iseof(self):
        if self.index >= len(self):
            return True
        return isinstance(self[self.index], Eof)

    def get(self, count):
        """
        """
        if self.index + count < len(self):
            return self[self.index + count]

    def reduce(self, ptree):
        """
        """
        count = self.index + ptree.tlen()

        del self[self.index: count]
        if isinstance(ptree, PTree) and ptree.type:
            self.insert(self.index, ptree)

    def clen(self):
        count = 0
        for ind in self:
            count += ind.clen()
        return count

class PTree(list):
    """
    """

    def __init__(self, rule, *args, type=[]):
        super(PTree, self).__init__(args)

        self.rule = rule
        self.type = type
        self.result = None

    def eval(self, handles):
        result = self
        for ind in handles:
            result = ind(*result)

        if result is not self:
            self.result = result 

    def val(self):
        return self.result

    def tlen(self):
        return len(self)

class Token(XNode):
    def __init__(self, value):
        self.value = value
        self.type = [self,]

    @classmethod
    def validate(cls, token):
        if isinstance(token, cls):
            return PTree(cls, token)

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
    def __init__(self, value):
        self.value = value

    def validate(self, token):
        if self.value == token.value:
            return token

class Eof(Token):
    pass

class Sof(Token):
    pass

eof = Eof('')
