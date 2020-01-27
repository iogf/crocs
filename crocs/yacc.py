from crocs.token import XNode, Token, eof, TokVal, PTree
import re
import time

class YaccError(Exception):
    pass

class Grammar:
    discard = []

class Yacc:
    def __init__(self, grammar):
        self.root    = grammar.root
        self.discard = grammar.discard

    def is_discarded(self, token):
        for indi in self.discard:
            if indi.consume((token, )):
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
        tokens = tuple(tokens)

        while True:
            ptree  = self.consume(tokens)
            tokens = tokens[ptree.tlen():]
            if ptree: 
                yield ptree
            else:
                break

    def consume(self, tokens):
        """
        """

        ptree = self.root.consume(tokens)
        if not ptree and tokens:
            if tokens[0]:
                self.handle_error(ptree, tokens)
        return ptree

    def handle_error(self, ptree, tokens):
        """
        """

        print('Crocs Yacc error!')
        print('PTree:', ptree)
        print('Tokens:', tokens)
        raise YaccError('Unexpected struct!')

    def add_handle(self, rule, handle):
        """
        """
        rule.hmap.append(handle)

    def del_handle(self, rule, handle):
        """
        """
        rule.hmap.remove(handle)

class Struct(XNode):
    def __init__(self, recursive=False):
        super(Struct, self).__init__()
        self.recursive = recursive
        self.structs = []
        self.rules   = []

    def consume(self, tokens, exclude=[], precedence=[]):
        """
        """

        ptree = self.match_structs(tokens, exclude, precedence)
        ptree = ptree if ptree else self.match_rules(
        tokens, exclude, precedence)

        if ptree and self.recursive:
            return self.reduce(ptree, tokens, precedence)
        return ptree

    def match_structs(self, tokens, exclude, precedence):
        for ind in self.structs:
            ptree = ind.consume(tokens, exclude, precedence)
            if ptree:
                return ptree
        return PTree(self)

    def match_rules(self, tokens, exclude, precedence):
        for ind in self.rules:
            if not (ind in exclude or ind in precedence):
                ptree = ind.consume(tokens, exclude, precedence)
                if ptree:
                    return ptree
        return PTree(self)

    def replace(self, ptree, tokens, precedence=[]):
        """
        """
        for ind in self.rules:
            if not ind in precedence:
                if ind.root is self:
                    rtree = ind.replace(ptree, tokens, precedence)
                    if rtree:
                        return rtree
        return PTree(self)

    def reduce(self, ptree, tokens, precedence=[]):
        """
        """

        rtree = None
        while True:
            rtree = self.replace(ptree, tokens, precedence)
            if not rtree:
                return ptree
            ptree = rtree

    def add(self, *args):
        """
        """
        for ind in args:
            if isinstance(ind, Struct):
                self.structs.append(ind)
            else:
                self.rules.append(ind)

class Rule(XNode):
    def __init__(self, root, *args, up=[]):
        """
        """
        self.root = root
        self.symbols = args
        self.up   = up
        self.hmap = []

    def replace(self, ptree, tokens, precedence=[]):
        """
        """

        tokens  = tokens[ptree.tlen():]
        exclude = [self]
        rtree = self.validate(ptree, tokens, 
            exclude, precedence=self.up)
        return rtree

    def validate(self, ptree, tokens, exclude=[], precedence=[]):
        """
        """

        ntree = PTree(self)
        ntree.append(ptree)

        for ind in self.symbols:
            rtree = ind.consume(tokens, exclude, precedence)
            if rtree:
                tokens = tokens[rtree.tlen():]
                ntree.append(rtree)
            else:
                return rtree
        ntree.eval(self.hmap)
        return ntree

    def consume(self, tokens, exclude=[], precedence=[]):
        """
        """

        if isinstance(self.root, Struct):
            exclude = exclude + [self]

        rtree = self.root.consume(tokens, exclude, self.up)
        if not rtree:
            return PTree(self)

        tokens = tokens[rtree.tlen():]
        ntree = self.validate(rtree, tokens, exclude, self.up)
        if not ntree and self.symbols:
            return PTree(self)
        return ntree

class Times(XNode):
    def __init__(self, refer):
        self.refer = refer

    def consume(self, tokens, exclude=[], precedence=[]):
        """
        """
        ptree = PTree(self)
        while True:
            rtree = self.refer.consume(tokens, exclude, precedence)
            if rtree:
                tokens = tokens[rtree.tlen():]
                ptree.append(rtree)
            else:
                return ptree

