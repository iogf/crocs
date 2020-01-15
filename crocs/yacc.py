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
        count = 0
        for ind in self:
            count += ind.tlen()
        return count

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

class LexMap(XNode):
    def __init__(self):
        """
        """
        self.children = []
        super(LexMap, self).__init__()

    def register(self, xnode):
        self.children.append(xnode)

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
        self.children = []
        super(Struct, self).__init__()
        self.recursive = recursive

    def consume(self, tokens, exclude=[], precedence=[]):
        """
        """

        for ind in self.children:
            if not ind in exclude and not ind in precedence:
                ptree = ind.consume(tokens, exclude, precedence)
                if ptree and self.recursive:
                    return self.reduce(ptree, tokens, precedence)
                elif ptree:
                    return ptree
        return PTree(self)

    def push(self, struct, ptree, tokens, precedence=[]):
        """
        """
        for ind in self.children:
            if not ind in precedence:
               rtree = ind.push(struct, ptree, tokens, precedence)
               if rtree:
                   return rtree
        return PTree(self)

    def reduce(self, ptree, tokens, precedence=[]):
        """
        """

        rtree = None
        while True:
            rtree = self.push(self, 
                ptree, tokens, precedence)
            if not rtree:
                return ptree
            ptree = rtree

    def add(self, *args):
        """
        """
        self.children.extend(args)

class Rule(XNode):
    def __init__(self, trigger, *args, up=[]):
        """
        """
        self.trigger = trigger
        self.symbols = args
        self.up   = up
        self.hmap = []

    def push(self, struct, ptree, tokens, precedence=[]):
        """
        """

        if not struct is self.trigger:
            return PTree(self)
    
        tokens  = tokens[ptree.tlen():]
        exclude = [self]
        rtree = self.validate(ptree, tokens, 
            exclude, precedence=self.up)
        return rtree

    def validate(self, ptree, tokens, exclude=[], precedence=[]):
        """
        """

        ntree = PTree(self, ptree)
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

        if isinstance(self.trigger, Struct):
            exclude = exclude + [self]

        rtree = self.trigger.consume(tokens, exclude, self.up)
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

    def consume(self, tokens, exclude=[]):
        """
        """
        ptree = PTree(self)
        while True:
            rtree = self.refer.consume(tokens, exclude)
            if rtree:
                ptree.append(rtree)
            else:
                return ptree
            tokens = tokens[rtree.tlen():]


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
