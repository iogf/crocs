from crocs.token import XNode, Token, eof, TokVal
import re
import time

class LexError(Exception):
    pass

class YaccError(Exception):
    pass

class Grammar:
    discard = []

class XSpec:
    pass

class TSeq(list):
    """
    This is meant to be returned by XNode's instances
    that extract strings from a given doc sequentially.
    """

    def __init__(self, *args):
        self.extend(args)
        self.slen = 0
        self.tlen = 0

    def clen(self):
        val = map(len, self)
        return sum(val)

    def __len__(self):
        return self.clen()

class PTree(list):
    """
    """

    def __init__(self, rule, *args):
        super(PTree, self).__init__(args)
        self.rule = rule

    def plen(self):
        count = 0
        for ind in self:
            count += ind.plen()
        return count

class Yacc:
    def __init__(self, grammar):
        self.root    = grammar.root
        self.discard = grammar.discard
        self.hmap    = dict()

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
        
    def exec_handles(self):
        pass

    def build(self, tokens):
        """
        """

        tokens = self.remove_tokens(tokens)
        tokens = tuple(tokens)

        while True:
            ptree  = self.consume(tokens)
            tokens = tokens[ptree.plen():]
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

    def add_handle(self, xnode, handle):
        """
        """
        handles = self.hmap.get(xnode, [])
        handles.append(handle)
        pass

    def del_handle(self, xnode, handle):
        """
        """
        handles = self.map[xnode]
        handles.remove(handle)

    def skip(self):
        pass

class Lexer:
    def __init__(self, xspec, no_errors=False):
        """
        """
        self.root   = xspec.root
        self.data   = ''
        self.offset = 0
        self.no_errorss = no_errors

    def run(self):
        """
        """

        while True:
            tseq = self.consume(self.data)
            self.data = self.data[len(tseq):]
            if tseq:
                yield from tseq
            else:
                break

        # The loop stops on eof. It is useful for
        # some rules.
        yield eof

    def consume(self, data):
        """
        """
        tseq = self.root.consume(data)
        if not tseq and data:
            self.handle_error()
        return tseq

    def handle_error(self):
        msg = 'Unexpected token: %s' % repr(self.data[:30])
        raise LexError(msg)

    def feed(self, data):
        """
        """
        self.data = data
        self.offset = 0

    def skip(self):
        """
        """
        pass

class LexMap(XNode):
    def __init__(self):
        """
        """
        super(LexMap, self).__init__()

    def consume(self, data):
        """
        """
        if not data:
            return TSeq(eof)

        for ind in self.children:
            tseq = ind.consume(data)
            if tseq:
                return tseq
        return TSeq()

    def __repr__(self):
        return 'LexMap(%s)' % self.children

class Struct(XNode):
    def __init__(self, recursive=False):
        super(Struct, self).__init__()
        self.recursive = recursive

    def consume(self, tokens, exclude=[]):
        """
        """

        for ind in self.children:
            if not ind in exclude:
                ptree = ind.consume(tokens, exclude)
                if ptree and self.recursive:
                    return self.reduce(ptree, tokens)
                elif ptree:
                    return ptree
        return PTree(self)

    def shift(self, struct, ptree, tokens):
        """
        """
        for ind in self.children:
            rtree = ind.shift(struct, ptree, tokens)
            if rtree:
                return rtree
        return PTree(self)

    def reduce(self, ptree, tokens):
        """
        """

        rtree = None
        while True:
            rtree = self.shift(self, ptree, tokens)
            if rtree:
                ptree = rtree
            else:
                return ptree

    def add(self, *args):
        """
        """
        self.children.extend(args)

class Rule(XNode):
    def __init__(self, trigger, *args):
        """
        """
        self.trigger = trigger
        self.syms  = args

    def shift(self, struct, ptree, tokens):
        """
        """

        if not struct is self.trigger:
            return PTree(self)

        slice = tokens[ptree.plen():]
        rtree = self.validate(slice, [self])
        if rtree:
            return  PTree(self, ptree, *rtree)
        return rtree

    def validate(self, tokens, exclude=[]):
        """
        """

        ptree = PTree(self)
        for ind in self.syms:
            slice = tokens[ptree.plen():]
            rtree = ind.consume(slice, exclude)
            if rtree:
                ptree.append(rtree)
            else:
                return PTree(self)
        return ptree

    def consume(self, tokens, exclude=[]):
        """
        """

        ptree = PTree(self)
        if isinstance(self.trigger, Struct):
            exclude = exclude + [self]

        rtree = self.trigger.consume(tokens, exclude)
        if not rtree:
            return PTree(self)

        slice = tokens[rtree.plen():]
        ntree = self.validate(slice, exclude)
        if not ntree and self.syms:
            return PTree(self)

        ptree.append(rtree)
        ptree.extend(ntree)
        return ptree

class Times(XNode):
    def __init__(self, refer):
        self.refer = refer

    def consume(self, tokens, exclude=[]):
        """
        """
        ptree = PTree(self)
        while True:
            slice = tokens[ptree.plen():]
            struct = self.refer.consume(slice, exclude)
            if struct:
                ptree.append(struct)
            else:
                return ptree

class LexSeq(XNode):
    """
    """
    def __init__(self, lexmap, *args, type=None):
        self.lexmap = lexmap
        self.xnodes = []
        self.type   = type
        self.xnodes.extend(args)
        lexmap.register(self)

    def consume(self, data):
        """
        """
        tseq = TSeq()
        for ind in self.xnodes:
            slice = data[len(tseq):]
            token = ind.consume(slice)
            if token:
                tseq.extend(token)
            else:
                return TSeq()
        pass

        if self.type:
            return TSeq(self.type(tseq))
        return tseq
        
    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes

class SeqNode(XNode):
    def __init__(self, regex, type=Token):
        """
        """

        super(XNode, self).__init__()
        self.regex = regex
        self.type  = type

    def consume(self, data):
        """
        """

        regobj = re.match(self.regex, data)
        if regobj:
            return self.mktoken(regobj)
                        
    def mktoken(self, regobj):
        tokval = regobj.group(0)
        token  = self.type(tokval)
        return TSeq(token)

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regex))

class LexNode(SeqNode):
    def __init__(self, lexmap, regex, type=Token):
        """
        """

        super(LexNode, self).__init__(regex, type)
        self.lexmap = lexmap
        self.lexmap.register(self)

class LexRef(XNode):
    def __init__(self, xnode):
        self.xnode = xnode
        super(LexRef, self).__init__()
        """
        """

    def consume(self, data):
        """
        """

        tseq = TSeq()
        while True:
            slice = data[len(tseq):]
            token = self.xnode.consume(slice)
            if not token:
                break
            else:
                tseq.extend(token)
        return tseq
