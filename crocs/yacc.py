from crocs.token import Token, eof, XNode
import re
import time

class LexError(Exception):
    pass

class YaccError(Exception):
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
    A parse tree, it is the result of a grammar rule
    validation. It contains the rule that was used to parse
    the tokens.
    """

    def __init__(self, rule, *args, types=set()):
        self.extend(args)
        self.rule = rule
        self.types = types
        self.value = self

    def tlen(self):
        count = 0
        for ind in self:
            count += ind.tlen()
        return count

    def plen(self):
        count = 0
        for ind in self:
            count += ind.plen()
        return count

class RTree(PTree):
    def __init__(self, ptree):
        self.extend(ptree)

        # The rule that evaluated an RTree is usually a 
        # PTree's type.
        self.rule = ptree.rule
        self.types = ptree.types
        self.value = self

        pass

    def plen(self):
        """
        An RTree is the result of evaluation of a Rule type against
        its grammar, a Rule type is a Grammar. 

        The length of a RTree is  1 otherwise it doesn't do slicing 
        of the tokens correctly.
        """

        return int(bool(self))

class Yacc:
    def __init__(self, grammar):
        self.grammar = grammar
        self.hmap    = dict()

    def is_discarded(self, token):
        for indi in self.grammar.discarded_tokens:
            if indi.consume((token, )):
                return True
        return False

    def discard_tokens(self, tokens):
        # Maybe discarding tokens should be here not
        # in grammar definition.
        for indi in tokens:
            if not self.is_discarded(indi):
                yield indi
        
    def build(self, tokens):
        tokens = self.discard_tokens(tokens)
        tokens = tuple(tokens)

        while True:
            ptree = self.consume(tokens)
            tokens = tokens[ptree.tlen():]
            if ptree: 
                yield ptree
            else:
                break

    def consume(self, tokens):
        ptree = self.grammar.consume(tokens)
        if not ptree and tokens:
            if tokens[0]:
                self.handle_error(ptree, tokens)
        return ptree

    def handle_error(self, ptree, tokens):
        print('Crocs Yacc error!')
        print('PTree:', ptree)
        print('Tokens:', tokens)
        raise YaccError('Unexpected struct!')

    def add_handle(self, xnode, handle):
        handles = self.hmap.get(xnode, [])
        handles.append(handle)
        pass

    def del_handle(self, xnode, handle):
        handles = self.map[xnode]
        handles.remove(handle)

    def skip(self):
        pass

class Lexer:
    def __init__(self, lexmap, no_errors=False):
        """
        """
        self.lexmap = lexmap
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
        tseq = self.lexmap.consume(data)
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

    def stop(self):
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

class Grammar(XNode):
    def __init__(self):
        super(Grammar, self).__init__()
        self.discarded_tokens = []
        self.stack = []

    def discard(self, *args):
        self.discarded_tokens.extend(args)

    def consume(self, tokens, exclude=[]):
        for ind in self.children:
            if not ind in exclude:
                ptree = ind.consume(tokens, exclude)
                if ptree:
                    return self.push(ptree, tokens)
        return PTree(self)

    def push(self, ptree, tokens):
        """
        """
        for ind in self.children:
            rtree = ind.push(ptree, tokens)
            if rtree:
                return rtree
        return ptree

    def is_refer(self):
        return True

    def add(self, *args):
        self.children.extend(args)

class Rule(XNode):
    def __init__(self, init, *args):
        """
        """
        self.init = init
        self.xnodes = args

    def push(self, ptree, tokens):
        if self.init.is_refer():
            return self.eval_ptree(ptree, tokens)

    def eval_ptree(self, ptree, tokens):
        mtree = PTree(self)                
        slice  = tokens[ptree.plen():]
        rtree = self.eval_xnodes(slice)
        if not rtree:
            return mtree

        mtree.append(ptree)
        mtree.extend(rtree)
        return mtree

    def eval_xnodes(self, tokens, exclude=[]):
        ptree = PTree(self)
        for ind in self.xnodes:
            slice  = tokens[ptree.plen():]
            struct = ind.consume(slice, exclude)
            if struct:
                ptree.append(struct)
            else:
                return PTree(self)
        return ptree

    def consume(self, tokens, exclude=[]):
        """
        """
        ptree = PTree(self)
        if self.init.is_refer():
            exclude = exclude + [self]

        struct = self.init.consume(tokens, exclude)
        if struct:
            ptree.append(struct)
        else:
            return ptree

        slice = tokens[ptree.plen():]
        struct = self.eval_xnodes(slice, exclude)

        if not struct and self.xnodes:
            return PTree(self)
        ptree.extend(struct)
        return ptree

class TokVal(XNode):
    def __init__(self, value, rule=None, types=set()):
        self.value = value
        self.rule = rule if rule else self
        self.types = types

    def consume(self, tokens, exclude=[]):
        if self.value == tokens[0].value:
            return tokens[0]

class Struct(XNode):
    def __init__(self, refer):
        self.refer = refer

    def is_refer(self):
        return True

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
