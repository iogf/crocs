from crocs.token import *
from collections.abc import Iterable
from crocs.token import *
import time

class YaccError(Exception):
    pass

class Grammar:
    discard = []

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

    def pop(self):
        pass
        
    def popleft(self, elem):
        pass

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
            yield index.elem
            index = index.next

    def back(self, index):
        if index.back is self.head:
            return index
        else:
            return index.back

    def delone(self, index):
        index.back.next = index.next
        indext.next.back = index.back

    def delete(self, index, lindex):
        index.back.next = lindex
        lindex.back = index.back

    def empty(self):    
        return self.head.next == self.last

    def first(self):
        return self.head.next

    def __str__(self):
        data = self.lst(self.head.next, self.last)
        data = list(data)
        return data.__str__()

    __repr__ = __str__

class Grouper:
    """
    """
    __slots__ = ['linked', 'index']

    def __init__(self):
        self.linked = LinkedList()
        self.index = None

    def expand(self, data):
        for ind in data:
            self.linked.append(ind)
        self.index = self.linked.first()

    def reset(self):
        self.index = self.linked.first()

    def clone(self):
        grouper = Grouper()
        grouper.linked = self.linked
        grouper.index = self.index
        return grouper

    def shift(self):
        self.index = self.linked.next(self.index)

    def shift_back(self):
        self.index = self.linked.back(self.index)

    def iseof(self):
        return self.index.islast()

    def get(self):
        """
        """
        lnode = self.index
        self.index = self.linked.next(self.index)
        
        if not lnode.islast():
            return lnode.elem

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

        data = self.remove_tokens(tokens)
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
        ptree   = self.validate(grouper)

        if not ptree:
            return None

        valid = self.lookahead(grouper)
        if valid:
            return None

        tokens.reduce(grouper.index, ptree)
        ptree.eval(self.hmap)
        return ptree

    def validate(self, tokens):
        ptree = PTree(rule=self, type=self.type)
        for ind in self.args:
            tok = ind.validate(tokens)
            if tok:
                ptree.append(tok)
            else:
                return None
        return ptree

    def lookahead(self, tokens):
        """
        """
        for ind in self.up:
            valid = ind.validate(tokens.clone())
            if valid:
                return True
        return False

class Times(XNode):
    def __init__(self, refer, min=1, max=None):
        self.refer = refer
        self.min = min
        self.max = max

    def validate(self, tokens):
        ptree = PTree(rule=self)

        while True:
            token = self.refer.validate(tokens)
            if not token:
                tokens.shift_back()
                if self.max and (self.min <= len(ptree) <= self.max):
                    return ptree
                elif self.min <= len(ptree):
                    return ptree
                else:
                    return 
