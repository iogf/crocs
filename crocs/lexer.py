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
        self.root   = xspec.root
        self.no_errorss = no_errors

    def feed(self, data):
        """
        """

        yield Sof('')
        while True:
            tseq = self.consume(data)
            if tseq:
                data = data[tseq.clen():]
                yield from tseq
            else:
                break

        # The loop stops on eof. It is useful for
        # some rules.
        yield Eof('')

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

    def register(self, xnode):
        self.children.append(xnode)

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
    """
    """
    def __init__(self, lexmap, *args):
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
    def __init__(self, regstr, type=Token, cast=None):
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
        tokval = regobj.group(0)
        token  = self.type(tokval, self.cast)
        return TSeq(token)

    def __repr__(self):
        return 'SeqNode(%s(%s))' % (
            self.type.__name__, repr(self.regstr))

class LexNode(SeqNode):
    def __init__(self, lexmap, regstr, type=Token, cast=None):
        """
        """

        super(LexNode, self).__init__(regstr, type, cast)
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
            token = self.xnode.consume(data)
            if token:
                data = data[token.clen():]
                tseq.extend(token)
            else:
                break
        return tseq
