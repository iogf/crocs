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

        yield Token('', Sof, offset=0)
        while True:
            tseq = self.consume(data)
            if tseq:
                data = data[tseq.clen():]
                yield from tseq
            else:
                break

        # The loop stops on eof. It is useful for
        # some rules.
        yield Token('', Eof, offset=self.offset)

    def consume(self, data):
        """
        """
        tseq = self.root.consume(data)
        if not tseq and data:
            self.handle_error(data)
        return tseq

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
        if not data:
            return None

        for ind in self.children:
            tseq = ind.consume(data)
            if tseq:
                return tseq

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
        tseq = TSeq()
        for ind in self.xnodes:
            token = ind.consume(data)
            if token:
                data = data[token.clen():]
                tseq.extend(token)
            else:
                return None
        return tseq
        
    def __repr__(self):
        return 'LexSeq(%s)' % self.xnodes

class SeqNode(XNode):
    def __init__(self, regstr, type=TokVal, cast=None):
        """
        """

        super(XNode, self).__init__()
        self.regex = re.compile(regstr)
        self.regstr = regstr
        self.type  = type
        self.cast  = cast

    def consume(self, data):
        """
        """

        regobj = self.regex.match(data)
        if regobj:
            return self.mktoken(regobj)
                        
    def mktoken(self, regobj):
        data  = regobj.group(0)
        token = Token(data, self.type, self.cast, Lexer.offset)
        Lexer.offset += token.clen()
        return TSeq(token)

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class LexNode(SeqNode):
    def __init__(self, regstr, type=TokVal, cast=None):
        """
        """

        super(LexNode, self).__init__(regstr, type, cast)

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
            token = self.xnode.consume(data)
            if token:
                data = data[token.clen():]
                tseq.extend(token)
            else:
                break
        return tseq
