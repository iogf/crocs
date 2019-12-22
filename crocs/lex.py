from crocs.token import Token, eof
import re
import time

class XNode:
    def __init__(self):
        self.expect = []
        self.root   = self

    def register(self, xnode):
        self.expect.append(xnode)
        xnode.root = self.root

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
            self.lexmap.eof()

    def process(self):
        token = self.lexmap.find(self.data)

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
        self.lexmap.clear()

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
        self.lnode   = self
        self.xstack  = []

    def clear(self):
        self.lnode  = self
        self.xstack.clear()

    def find(self, data):
        """
        """
        assert data != '', 'Crocs: String is empty!'

        token = self.consume(data)
        if not token and self.xstack:
            token = self.consume_xstack(data)

        if not token:
            self.handle_err(data)
        return token

    def eof(self):
        if self.xstack:
            self.handle_err('')

    def consume(self, data):
        for ind in self.lnode.expect:
            token = ind.consume(data)
            if token:
                return token

    def consume_xstack(self, data):
        """
        """

        self.lnode = self.xstack.pop()
        token = self.consume(data)

        return token

    def set_lnode(self, xnode):
        """
        """
        if isinstance(self.lnode, LexLink):
            self.xstack.append(self.lnode) 
        self.lnode = xnode

    def reset(self):
        self.lnode = self

    def handle_err(self, data):
        print('Crocs: Errors!') 
        print('> Expected: %s' % (self.expect + self.xstack[-1:]))
        print('> Data: %s' % repr(data))
        print('> Xstack:%s' % self.xstack)


class LexNode(LexMap):
    def __init__(self, xnode, regex, type=Token):
        """
        """
        err0 = 'Crocs: Invalid xnode value!'
        assert isinstance(xnode, (LexMap, LexNode)), err0

        err1 = 'Crocs: Invalid regex value'
        assert isinstance(regex, str), err1

        super(LexNode, self).__init__()
        self.regex = regex
        self.type  = type

        xnode.register(self)

    def consume(self, data):
        """
        """

        regobj = re.match(self.regex, data)
        if regobj:
            return self.mktoken(regobj)
                
    def mktoken(self, regobj):
        tokval = regobj.group(0)
        token  = self.type(tokval)

        if self.expect:
            self.root.set_lnode(self)
        else:
            self.root.reset()
        return token

    def __repr__(self):
        return '(%s, %s)' % (self.type.__name__, repr(self.regex))

class LexLink(LexMap):
    def __init__(self, xnode, lexmap):
        """
        """
        err0 = 'Crocs: Invalid xnode value!'
        assert isinstance(xnode, LexNode), err0
    
        err1 = 'Crocs: Invalid rnode value!'
        assert isinstance(lexmap, LexMap), err1

        super(LexLink, self).__init__()
        xnode.register(self)

        self.lexmap = lexmap

    def consume(self, data):
        """
        """
        self.lexmap.set_lnode(self)
        self.lexmap.set_lnode(self.lexmap)

        token = self.lexmap.consume(data)
        return token

    def __repr__(self):
        return '%s' % self.expect
