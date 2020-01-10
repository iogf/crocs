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

    def __init__(self, rule, *args):
        self.extend(args)
        self.rule = rule
        pass

    def tlen(self):
        count = 0
        for ind in self:
            count += ind.tlen()
        return count

class RTree(PTree):
    def __init__(self, ptree, type):
        self.extend(ptree)

        # The rule that evaluated an RTree is usually a 
        # PTree's type.
        self.rule = type
        pass

    def tlen(self):
        """
        An RTree is the result of evaluation of a Rule type against
        its grammar, a Rule type is a Grammar. 

        The length of a RTree is  1 otherwise it doesn't do slicing 
        of the tokens correctly.
        """
        return 1
        
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

    def consume(self, tokens, exclude=[]):
        if tokens[0].rule == self:
            return tokens[0]

        return self.validate(tokens, exclude)

    def validate(self, tokens, exclude=[]):
        for ind in self.children:
            if not ind in exclude:
               ptree = ind.consume(tokens, exclude)
               if ptree:
                   return ptree
        return PTree(self)

    def is_refer(self):
        return True

    def add(self, *args):
        self.children.extend(args)

class Rule(XNode):
    def __init__(self, *args, type=None):
        """
        """
        self.xnodes = []
        self.xnodes.extend(args)
        self.type = type

    def consume(self, tokens, exclude=[]):
        """
        It receives a sequence of tokens and attempt to match
        the specified rule.
    
        When there is a match and a type is defined then it prepends 
        the rule tokens to the tokens sequence and attempt to match 
        again with some rule in the grammar.

        It returns PTree's which may contain RTree's
        or Token's. An RTree is the result of a Rule type
        evaluation.
        """

        ptree = PTree(self)
        if self.xnodes[0].is_refer():
            exclude = exclude + [self]

        for ind in self.xnodes:
            slice  = tokens[ptree.tlen():]
            struct = ind.consume(slice, exclude)
            if struct:
                ptree.append(struct)
            else:
                return PTree(self)

        if self.type:
            return self.evaltype(ptree, tokens)
        return ptree

    def evaltype(self, ptree, tokens):
        """
        Consume returns a PTree that contains rule tokens,
        these rules are evaluated to a type. 

        The grammar rules may have rules that depend on this type. 
        Thus it has to be evaluated again. The PTree is prepended then 
        sent back to be matched.

        When there is no match against the rule type and its
        grammar then it returns the rule ptree.
        """

        slice = tokens[ptree.tlen():]            
        rtree = RTree(ptree, self.type)

        slice = (rtree, ) + slice
        rtree = self.type.validate(slice)
        if rtree:
            return rtree
        return ptree

class TokVal(XNode):
    def __init__(self, value, rule=None, type=None):
        self.value = value
        self.rule = rule if rule else self
        self.type = type

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
            slice = tokens[ptree.tlen():]
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
