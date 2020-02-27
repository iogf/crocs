from crocs.token import *
import re

class LexError(Exception):
    pass

class XSpec:
    pass

class Lexer:
    offset = 0
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

    def consume(self, data):
        """
        """
        tseq = self.root.consume(data)
        yield from tseq

        # if data:
            # self.handle_error(data)

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

class LexSeq(XNode):
    def __init__(self, *args):
        self.xnodes = []
        self.type   = type
        self.xnodes.extend(args)

    def consume(self, data):
        """
        """
        pass
        
    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes

class LexNode(XNode):
    def __init__(self, regstr, type=TokVal, cast=None):
        """
        """

        super(XNode, self).__init__()
        self.regex = re.compile(regstr)
        self.regstr = regstr
        self.type  = type
        self.cast  = cast
        self.offset = 0

    def consume(self, data):
        """
        """
        self.offset = 0
        while True:
            data, tok = self.mktoken(data)
            if tok:
                yield tok
            else:
                break

    def mktoken(self, data):
        regobj = self.regex.search(data)
        if not regobj:
            return data, None

        tokstr  = regobj.group(0)
        self.offset = self.offset + regobj.end()
        data = data[regobj.end():]

        token = Token(tokstr, self.type, self.cast, self.offset)
        return data, token

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))
