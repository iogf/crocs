from crocs.token import Token, eof
import re
import time

class LexError(Exception):
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

    def __len__(self):
        val = map(len, self)
        return sum(val)

class Yacc:
    def __init__(self, grammar):
        self.grammar = grammar

    def add_handle(self, xnode):
        pass

    def del_handle(self, xnode):
        pass

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
        self.children = []

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
        pass

class RuleMap(Grammar):
    """
    """
    def __init__(self, grammar, *args):
    
        pass

    def consume(self, data):
        pass

class Rule(XNode):
    def __init__(self, grammar, *args):
        pass

    def consume(self, data):
        pass

class LexSeq(XNode):
    """
    """
    def __init__(self, lexmap, *args, type=TSeq):
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

class Link(XNode):
    def __init__(self, xnode):
        self.xnode = xnode
        super(LexRef, self).__init__()
        """
        """

    def consume(self, data):
        """
        """
        pass

