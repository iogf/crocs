from crocs.token import *
import re

class LexError(Exception):
    pass

class XSpec:
    pass

class Lexer:
    def __init__(self, xspec):
        """
        """
        self.root       = xspec.root
        self.discarded  = xspec.root

    def feed(self, data):
        """
        """
        yield Token('', Sof)
        tseq = self.process(data)
        yield from tseq
        yield Token('', Eof)

    def process(self, data):
        pos = 0
        while True:
            tseq = self.consume(data, pos)
            if tseq:
                yield from tseq
                pos = tseq[-1].end
            elif pos != len(data):
                self.handle_error(data, pos)
            else:
                break

    def consume(self, data, pos):
        """
        """
        for ind in self.root:
            tseq = ind.consume(data, pos)
            if tseq:
                return tseq

    def handle_error(self, data, pos):
        msg = 'Unexpected token: %s' % repr(data[pos:pos+30])
        raise LexError(msg)

class LexMap(XNode):
    def __init__(self):
        """
        """
        self.children = []
        super(LexMap, self).__init__()

    def add(self, *args):
        self.children.extend(args)

    def consume(self, data, pos):
        """
        """
        for ind in self.children:
            tseq = ind.consume(data, pos)
            if tseq:
                return tseq

    def __repr__(self):
        return 'LexMap(%s)' % self.children

class LexLink(XNode):
    def __init__(self, lex):
        self.lex = lex

    def consume(self, data, pos):
        tseq = TSeq()
        while True:
            token = self.lex.consume(data, pos)
            if token:
                tseq.extend(token)
            else:
                break
            pos = token[-1].end
        return tseq

class LexNode(XNode):
    def __init__(self, regstr, type=TokVal, cast=None):
        """
        """
        super(XNode, self).__init__()
        self.regex  = re.compile(regstr)
        self.regstr = regstr
        self.type   = type
        self.cast   = cast
        self.match  = self.regex.match

    def consume(self, data, pos):
        regobj = self.match(data, pos)
        if regobj:
            return self.mktoken(regobj)

    def mktoken(self, regobj):
        token = Token(regobj.group(), self.type, 
        self.cast, regobj.start(), regobj.end())
        return TSeq((token,))

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class SeqNode(LexNode):
    def __init__(self, regstr, type=TokVal, cast=None):
        super(SeqNode, self).__init__(regstr, type, cast)

class LexSeq(XNode):
    def __init__(self, *args):
        self.args = args

    def consume(self, data, pos):
        tseq = TSeq()
        for ind in self.args:
            token = ind.consume(data, pos)
            if token:
                tseq.extend(token)
            else:
                return None
            pos = tseq[-1].end
        return tseq

    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes

