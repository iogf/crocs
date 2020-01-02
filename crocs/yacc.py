from crocs.token import Token, eof
import re
import time

class LexError(Exception):
    pass

class YaccError(Exception):
    pass

class XNode:
    def __init__(self):
        self.children = []

    def register(self, xnode):
        self.children.append(xnode)
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

    # def __bool__(self):
        # pass

    def clen(self):
        pass

    def __len__(self):
        val = map(len, self)
        return sum(val)

class PTree(list):
    """
    A parse tree, it is the result of a grammar rule
    validation. It contains the rule that was used to parse
    the tokens.
    """

    def __init__(self, rule, *args):
        self.extend(args)
        self.rule = rule
        pass

    def tlen(self):
        count = 0
        for ind in self:
            count += ind.tlen()
        return count

class Yacc:
    def __init__(self, grammar):
        self.grammar = grammar
        self.hmap    = dict()

    def discard_tokens(self, tokens):
        for indi in tokens:
            for indj in self.grammar.discarded_tokens:
                if not indj.consume((indi, )):
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
        print('Error!')
        print('PTree:', ptree)
        print('Data:', tokens)

    def add_handle(self, xnode, handle):
        handles = self.hmap.get(xnode, [])
        handles.append(handle)
        pass

    def del_handle(self, xnode, handle):
        handles = self.map[xnode]
        handles.remove(handle)

    def skip(self):
        pass

    def next(self):
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

    def discard(self, *args):
        self.discarded_tokens.extend(args)

    def consume(self, data):
        for ind in self.children:
            ptree = ind.consume(data)
            if ptree:
                return ptree
        return PTree(self)

class Rule(XNode):
    def __init__(self, grammar, *args):
        self.xnodes = []
        self.xnodes.extend(args)
        grammar.register(self)

    def consume(self, tokens):
        ptree = PTree(self)
        for ind in self.xnodes:
            slice = tokens[ptree.tlen():]
            struct = ind.consume(slice)
            if struct:
                ptree.append(struct)
            else:
                return PTree(self)
        return ptree

class TokVal:
    def __init__(self, value):
        self.value = value

    def consume(self, tokens):
        if self.value == tokens[0].value:
            return tokens[0]
        # print(repr(self.value), repr(tokens[0].value))

class Struct(XNode):
    def __init__(self, *args):
        pass

    def validate(self, data):
        pass

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
