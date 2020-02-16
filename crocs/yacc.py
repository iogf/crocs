from crocs.token import *
from collections.abc import Iterable
from crocs.token import *
import time

class YaccError(Exception):
    pass

class Grammar:
    discard = []

class Grouper:
    """
    """

    def __init__(self, data):
        self.data  = data
        self.index = 0

    def reset(self):
        self.index = 0

    def clone(self):
        grouper = Grouper(self.data)
        grouper.index = self.index
        return grouper

    def shift(self, index=1):
        self.index = self.index + index

    def iseof(self):
        if self.index >= len(self.data):
            return True
        else:
            return False

    def get(self):
        """
        """
        if self.index >= len(self.data):
            return None

        tok = self.data[self.index]
        self.index += 1
        return tok

    def reduce(self, ptree):
        """
        """
        count = self.index + len(ptree)
        del self.data[self.index: count]
        if ptree.type:
            self.data.insert(self.index, ptree)

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()

class Yacc:
    def __init__(self, grammar):
        self.root    = grammar.root
        self.discard = grammar.discard

    def is_discarded(self, token):
        for indi in self.discard:
            if indi.istype(token):
                return True
        return False

    def remove_tokens(self, tokens):
        """
        """
        for indi in tokens:
            if not self.is_discarded(indi):
                yield indi
        
    def build(self, tokens):
        """
        """

        tokens = self.remove_tokens(tokens)
        tokens = Grouper(list(tokens))
        
        ptree = self.process(tokens)
        yield from ptree

        if tokens.data:
            self.handle_error(tokens)

    def process(self, tokens):
        while True:
            ptree = self.consume(tokens)
            if ptree:
                yield ptree
                if ptree.type:
                    tokens.reset()
            elif not tokens.iseof():
                tokens.shift()
            else:
                break

    def consume(self, tokens):
        """
        """
        for ind in self.root:
            ptree = ind.consume(tokens)
            if ptree:
                return ptree
                            
    def handle_error(self, tokens):
        """
        """
        print('Crocs Yacc error!')
        print('Tokens:', tokens)
        raise YaccError('Unexpected struct!')

    def add_handle(self, rule, handle):
        """
        """
        rule.hmap = handle

    def del_handle(self, rule, handle):
        """
        """
        rule.hmap = handle

class Struct(XNode):
    def __init__(self):
        super(Struct, self).__init__()
        self.rules = []

    def validate(self, tokens):
        tok = tokens.get()
        if tok and self is tok.type:
            return tok

    def consume(self, tokens):
        """
        """
        
        for ind in self.rules:
            ptree = ind.consume(tokens)
            if ptree:
                return ptree

    def add(self, *args):
        """
        """
        self.rules.extend(args)

class Rule(XNode):
    def __init__(self, *args, up=(), type=None):
        """
        """
        self.args = args
        self.type = type
        self.hmap = None
        self.up   = []

        self.up.extend(up)

    def consume(self, tokens):
        """
        """

        grouper = tokens.clone()

        ptree = self.validate(grouper)
        if not ptree:
            return None

        ntree = self.lookahead(grouper)
        if ntree:
            return None

        tokens.reduce(ptree)
        ptree.eval(self.hmap)
        return ptree

    def validate(self, tokens):
        ntree = PTree(rule=self, type=self.type)
        for ind in self.args:
           ptree = ind.validate(tokens)
           if ptree:
               ntree.append(ptree)
           else:
               return None
        return ntree

    def lookahead(self, tokens):
        """
        """
        for ind in self.up:
            ptree = ind.validate(tokens.clone())
            if ptree:
                return ptree

class Times(XNode):
    def __init__(self, refer):
        self.refer = refer

    def consume(self, tokens, exclude=[], precedence=[]):
        """
        """
        pass

