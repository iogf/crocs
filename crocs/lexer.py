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
        self.offset = 0
        yield Token('', Sof)
        tseq = self.consume(data)
        tseq = sorted(tseq, key=lambda ind: ind.offset)

        yield from tseq
        yield Token('', Eof)

    def validate(self, tseq):
        """
        """
            # self.handle_error(data)
        pass

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
    def __init__(self, regstr, type=TokVal, cast=None):
        """
        """

        super(XNode, self).__init__()
        self.regex = re.compile(regstr)
        self.regstr = regstr
        self.type  = type
        self.cast  = cast
        self.pos = 0

    def consume(self, data):
        """
        """
        self.pos = 0
        while True:
            regobj = self.regex.search(data, self.pos)
            if regobj:
                yield self.mktoken(regobj)
            else:
                break

    def mktoken(self, regobj):
        self.pos = regobj.end()
        token = Token(regobj.group(), self.type, 
        self.cast, regobj.end())
        return token

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class SeqNode(LexNode):
    def __init__(self, regstr, type=TokVal, cast=None):
        super(SeqNode, self).__init__(regstr, type, cast)

    def validate(self, data, pos):
        regobj = self.regex.match(data, pos)
        if regobj:
            return self.mktoken(regobj)

    def index(self, data, pos):
        regobj = self.regex.search(data, pos)
        if regobj:
            return self.mktoken(regobj)

class LexSeq(XNode):
    def __init__(self, *args):
        self.args = args
        self.pos  = 0

    def consume(self, data):
        self.pos = 0
        tseq = None
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
            token = ind.validate(tseq[-1].pos, data)
            if token:
                tseq.append(token)
            else:
                return None
        self.pos = tseq[-1]
        return tseq

    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes
