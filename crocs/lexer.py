from crocs.token import *
import re

class LexError(Exception):
    pass

class XSpec:
    pass

class Lexer:
    def __init__(self, xspec, no_errors=False):
        """
        """
        self.root       = xspec.root
        self.discarded  = xspec.root
        self.no_errorss = no_errors

    def feed(self, data):
        """
        """
        yield Token('', Sof)
        tseq = self.consume(data)
        tseq = sorted(tseq, key=lambda ind: ind.pos)
        tseq = self.validate(tseq)
        yield from tseq
        yield Token('', Eof)

    def normalize(self, tseq):
        tseq = list(tseq)
        for ind in range(0, len(tseq) - 1):
            if tseq[ind].start > tseq[ind+1].start:
                if tseq[ind].end < tseq[ind+1].end:
                    continue

    def validate(self, tseq):
        """
        """
        for ind in range(0, len(tseq) - 1):
            if tseq[ind].end == tseq[ind+1].start:
                yield ind
            else:
                self.handle_error(data)

    def consume(self, data):
        """
        """
        for ind in self.root:
            tseq = ind.consume(data)
            yield from tseq

    def handle_error(self, data):
        msg = 'Unexpected token: %s' % repr(data[:30])
        raise LexError(msg)

class LexMap(XNode):
    def __init__(self):
        """
        """
        self.children = []
        super(LexMap, self).__init__()

    def add(self, *args):
        self.children.extend(args)

    def consume(self, data):
        """
        """
        for ind in self.children:
            token = ind.consume(data)
            yield from token

    def __repr__(self):
        return 'LexMap(%s)' % self.children

class LexNode(XNode):
    def __init__(self, regstr, type=TokVal, cast=None, up=()):
        """
        """

        super(XNode, self).__init__()
        self.regex  = re.compile(regstr)
        self.regstr = regstr
        self.type   = type
        self.cast   = cast
        self.pos    = 0
        self.up     = up
        self.search = self.regex.search
        self.match  = self.regex.match

    def consume(self, data):
        """
        """
        self.pos = 0
        while True:
            regobj  = self.validate(data)
            if regobj:
                self.pos = regobj.end()
            else:
                token = self.mktoken(data)
                if token:
                    yield token
                else:
                    break

    def validate(self, data):
        for ind in self.up:
            regobj = ind.startswith(data, self.pos)
            if regobj:
                return regobj
        return None

    def startswith(self, data, pos):
        regobj = self.match(data, pos)
        return regobj

    def mktoken(self, data):
        regobj = self.search(data, self.pos)
        if not regobj:
            return None

        self.pos = regobj.end()
        token = Token(regobj.group(), self.type, 
        self.cast, regobj.start(), regobj.end())
        return token

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class SeqNode(LexNode):
    def __init__(self, regstr, type=TokVal, cast=None):
        super(SeqNode, self).__init__(regstr, type, cast)

    def mktoken(self, data, pos):
        regobj = self.match(data, pos)
        if regobj:
            return Token(regobj.group(), self.type, 
                self.cast, regobj.start(), regobj.end())

    def index(self, data, pos):
        regobj = self.search(data, pos)
        if regobj:
            return Token(regobj.group(), self.type, 
                self.cast, regobj.start(), regobj.end())

class LexSeq(XNode):
    def __init__(self, *args):
        self.args = args
        self.pos  = 0

    def consume(self, data):
        self.pos = 0
        tseq = True
        while tseq:
            tseq = self.loop(data)
            if tseq:
                yield from tseq

    def loop(self, data):
        tseq  = TSeq()
        token = self.args[0].index(data, self.pos)
        if not token:
            return None

        tseq.append(token)
        for ind in self.args[1:]:
            token = ind.mktoken(data, tseq[-1].end)
            if token:
                tseq.append(token)
            else:
                return None
        self.pos = tseq[-1].end
        return tseq

    def startswith(self, data, pos):
        regobj = self.args[0].startswith(data, pos)
        if not regobj:
            return None

        for ind in self.args[1:]:
            regobj = ind.startswith(data, regobj.end())
            if not regobj:
                return None
        return regobj

    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes
