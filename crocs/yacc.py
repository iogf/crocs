from crocs.token import *
from collections.abc import Iterable
from crocs.token import *
import time

class YaccError(Exception):
    pass

class Grammar:
    pass

class LinkedNode:
    __slots__ = ['elem', 'next', 'back']
    def __init__(self, elem, back=None, next=None):
        self.elem = elem
        self.next = next
        self.back = back

    def islast(self):
        return False

class HeadNode:
    def __init__(self):
        self.next = None

class LastNode:
    def __init__(self):
        self.back = None

    def islast(self):
        return True

class LinkedList:
    def __init__(self):
        self.head = HeadNode()
        self.last = LastNode()
        self.head.next = self.last
        self.last.back = self.head

    def append(self, elem):
        lnode = LinkedNode(elem, self.last.back, self.last)
        self.last.back.next = lnode
        self.last.back = lnode
        return lnode

    def appendleft(self, elem):
        lnode = LinkedNode(elem, self.head, self.head.next)
        self.head.next.back = lnode
        self.head.next = lnode
        return lnode

    def insert(self, index, elem):
        lnode = LinkedNode(elem, index.back, index)
        index.back.next = lnode
        index.back = lnode
        return lnode

    def next(self, index):
        if index is self.last:
            return index
        else:
            return index.next

    def lst(self, index, lindex):
        while index != lindex:
            yield index
            index = index.next

    def back(self, index):
        if index.back is self.head:
            return index
        else:
            return index.back

    def delete(self, index, lindex):
        index.back.next = lindex
        lindex.back = index.back

    def empty(self):    
        return self.head.next == self.last

    def first(self):
        return self.head.next

    def __str__(self):
        data = self.lst(self.head.next, self.last)
        data = list(map(lambda ind: ind.elem, data))
        return data.__str__()

    __repr__ = __str__

class Slice:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.index = start

    def get(self):
        if self.index == self.end:
            return None

        elem = self.index.elem
        self.shift()
        return elem

    def shift(self):
        if self.index != self.end:
            self.index = self.index.next

    def lshift(self):
        if self.index != self.start:
            self.index = self.index.back
        
class Grouper:
    """
    """

    def __init__(self):
        self.linked = LinkedList()
        self.index = None

    def expand(self, tokens):
        for ind in tokens:
            self.linked.append(ind)
        self.index = self.linked.first()

    def reset(self):
        self.index = self.linked.first()

    def shift(self):
        self.index = self.linked.next(self.index)

    def match(self, rule):
        index, ptree = self.validate(self.index, rule)
        if not ptree:
            return None

        if rule.up:
            valid = self.lookahead(index, rule)
            if not valid:
                return None

        ptree.eval(rule.hmap)
        self.reduce(index, ptree)
        return ptree

    def validate(self, lindex, rule):
        ptree = PTree(rule.type)
        slc   = Slice(lindex, self.linked.last)

        for ind in rule.args:
            token = ind.validate(slc)
            if token:
                ptree.append(token)
            else:
                return slc.index, None
        return slc.index, ptree

    def lookahead(self, lindex, rule):
        for ind in rule.up:
            index, ptree = self.validate(lindex, ind)
            if ptree:
                return False
        return True

    def reduce(self, lindex, ptree):
        """
        """

        if ptree.type:
            self.replace(lindex, ptree)
        else:
            self.delete(lindex)

    def delete(self, lindex):
        self.linked.delete(self.index, lindex)
        self.index = lindex

    def replace(self, lindex, ptree):
        self.linked.delete(self.index, lindex)
        self.linked.insert(lindex, ptree)
        self.index = lindex

    def __str__(self):
        return self.linked.__str__()

    __repr__ = __str__

class Yacc:
    def __init__(self, grammar):
        self.root = grammar.root
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

        data = self.remove_tokens(tokens)
        data = list(data)
        tokens = Grouper()
        tokens.expand(data)

        ptree = self.process(tokens)
        yield from ptree

        if not tokens.linked.empty():
            self.handle_error(tokens)

    def process(self, tokens):
        while True:
            ptree = self.consume(tokens)
            if ptree:
                yield ptree
                if ptree.type:
                    tokens.reset()
            elif tokens.linked.empty():
                break
            elif not tokens.index.islast():
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

    def istype(self, tok):
        if self is tok.type:
            return tok

    def validate(self, slc):
        tok = slc.get()
        if tok and tok.type is self:
            return tok

    def consume(self, tokens):
        """
        """
        
        for ind in self.rules:
           ptree = tokens.match(ind)
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

class Group(XNode):
    def __init__(self, token, min=1, max=None):
        self.token = token
        self.min = min

        self.max = max

    def validate(self, slc):
        ptree = PTree(None)
        while True:
            token = self.token.validate(slc)
            if token:
                ptree.append(token)
            elif self.max and self.min <= len(ptree) < self.max:
                slc.lshift()
                return ptree
            elif not self.max and self.min <= len(ptree):
                slc.lshift()
                return ptree
            else:
                return


