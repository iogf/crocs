from crocs.core import XNode, Token, eof, TokVal, TSeq, PTree, Sof
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
            if indi.validate(token):
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
        tokens = list(tokens)
        tokens = TSeq(*tokens)
        tokens.insert(0, Sof(''))

        while True:
            ptree = self.process(tokens)
            if not ptree and tokens:
                self.handle_error(tokens)
            elif tokens:
                yield from ptree
            else:
                break

    def process(self, tokens):
        data = []
        tokens.reset()
        
        while True:
            ptree = self.consume(tokens)
            if ptree:
                data.extend(ptree)
            elif not tokens.iseof():
                tokens.shift()
            else:
                return data

    def consume(self, tokens):
        """
        """
        data = []
        for ind in self.root:
            ptree = ind.consume(tokens)
            if ptree:
                data.extend(ptree)
        return data
            
    def handle_error(self, tokens):
        """
        """

        print('Crocs Yacc error!')
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
    def __init__(self):
        super(Struct, self).__init__()
        self.rules   = []

    def validate(self, tok):
        if self in tok.type:
            return tok

    def consume(self, tokens):
        """
        """
        
        data = []
        for ind in self.rules:
            ptree = ind.consume(tokens)
            if ptree:
                data.append(ptree)
        return data                  

    def add(self, *args):
        """
        """
        self.rules.extend(args)

class Rule(XNode):
    def __init__(self, *args, type=[]):
        """
        """
        self.args = args
        self.type = type
        self.hmap = []

    def consume(self, tokens):
        """
        """

        ntree = PTree(self, type=self.type)
        count = 0
        for ind in self.args:
            tok = tokens.get(count)
            if tok == None:
                return None
            ptree = ind.validate(tok)
            if ptree:
                ntree.append(ptree)
            else:
                return None
            count = count + 1
        tokens.reduce(ntree)
        ntree.eval(self.hmap)
        return ntree

class Times(XNode):
    def __init__(self, refer):
        self.refer = refer

    def consume(self, tokens, exclude=[], precedence=[]):
        """
        """
        pass

