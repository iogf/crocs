from crocs.token import Token, eof
import re
import time

class XNode:
    pass

class Lexer:
    def __init__(self, lexmap):
        """
        """
        self.lexmap = lexmap
        self.data   = None
        self.offset = 0

    def next(self):
        """
        """

        if self.data:
            return self.process()
        else:
            self.lexmap.is_error()

    def process(self):
        token = self.lexmap.consume(self.data)

        if token:
            self.slice(token)
        return token

    def slice(self, token):
        size = len(token.value)
        self.data = self.data[size:]

    def run(self):
        """
        """
        while True:
            token = self.next()
            if token:
                yield token
            else:
                break

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
    def __init__(self, xnode=None, handle_err=None):
        """
        """

        self.xnode    = xnode
        self.children = []
        self.expect = self
        self.xstack = []
        self.root = self

        if handle_err:
            self.handle_err = handle_err 

        if xnode:
            xnode.register(self)

    def register(self, xnode):
        self.children.append(xnode)
        xnode.root = self.root

    def consume(self, data):
        assert data != '', 'Crocs: No valid data!'

        for ind in self.expect.children:
            token = ind.is_valid(data)
            if token:
                return token

        if self.xstack and data:
            return self.consume_refs(data)

        self.handle_err(data)

    def consume_refs(self, data):
        self.expect = self.xstack.pop()
        token = self.consume(data)

        return token

    def set_expect(self, xnode):
        """
        """
        if isinstance(self.expect, LexLink):
            self.xstack.append(self.expect) 
        self.expect = xnode

    def reset(self):
        self.expect = self

    def is_error(self):
        if self.xstack:
            print('Expected: %s\nFound Eof!' %
                self.xstack)

    def handle_err(self, data):
        print('> Invalid token.')
        print('> Expected:', self.children)
        print('> Data:', repr(data))

class LexNode(LexMap):
    def __init__(self, xnode, regex, type=Token, handle_err=None):
        """
        """
        err0 = 'Crocs: Invalid xnode value!'
        assert isinstance(xnode, (LexMap, LexNode)), err0

        err1 = 'Crocs: Invalid regex value'
        assert isinstance(regex, str), err1

        super(LexNode, self).__init__(xnode, handle_err)
        self.regex    = regex
        self.type     = type

    def is_valid(self, data):
        """
        """

        regobj = re.match(self.regex, data)
        if regobj:
            return self.handle_token(regobj)
                
    def handle_token(self, regobj):
        token = self.type(regobj.group(0))

        if self.children:
            self.root.set_expect(self)
        else:
            self.root.reset()

        return token

    def __repr__(self):
        return '(%s %s)' % (self.type, self.regex)

class LexLink(LexMap):
    def __init__(self, xnode, rnode, handle_err=None):
        """
        """
        err0 = 'Crocs: Invalid xnode value!'
        assert isinstance(xnode, LexNode), err0
    
        err1 = 'Crocs: Invalid rnode value!'
        assert isinstance(rnode, LexMap), err1

        super(LexLink, self).__init__(xnode, handle_err)
        self.rnode = rnode
        self.expect = self

    def is_valid(self, data):
        """
        """
        self.rnode.set_expect(self)
        self.rnode.set_expect(self.rnode)

        token = self.rnode.consume(data)
        return token
