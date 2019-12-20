import re
import time

class XNode:
    pass

class Lexer:
    def __init__(self, lexmap):
        """
        """
        self.lexmap = lexmap

        # Last regex node that was matched.
        self.lnode = lexmap
        self.data  = None
        self.offset = 0

    def token(self):
        """
        """

        state = self.lnode.consume(self.data)
        if state: 
            return self.mktoken(state)
        if self.data and self.lnode.children:
            self.display_error()

    def display_error(self):
        """
        """
        self.lnode.on_err()
        print('Data: %s ...' % self.data[:40])

    def mktoken(self, state):
        """
        """

        tokval, self.data, xnode = state
        self.set_rule(xnode)

        if xnode.type: 
            return xnode.type(tokval)
        return self.token()
    
    def run(self):
        """
        """

        while True:
            token = self.token()
            if token:
                yield token
            else:
                break

    def feed(self, data):
        """
        """
        self.data = data
        self.offset = 0

    def set_rule(self, xnode):
        if not xnode.children:
            self.lnode = self.lexmap
        else:
            self.lnode = xnode

    def skip(self):
        """
        """
        pass

    def stop(self):
        pass

class LexMap(XNode):
    def __init__(self, xnode=None, msgerr=None):
        """
        """

        self.xnode    = xnode
        self.children = []
        self.msgerr   = msgerr

        if xnode:
            self.xnode.children.append(self)

    def consume(self, data):
        for ind in self.children:
            state = ind.is_valid(data)
            if state:
                return state

    def on_err(self):
        default_msgerr = 'Unrecognized token!'
        if self.msgerr:
            print(self.msgerr)
        else:
            print(default_msgerr)

class LexNode(LexMap):
    def __init__(self, xnode, regex, type=None):
        """
        """

        self.xnode    = xnode
        self.regex    = regex
        self.type     = type
        self.children = []
        self.xnode.children.append(self)

    def is_valid(self, data):
        """
        """

        rmatch = re.match(self.regex, data)
        if rmatch:
            return (rmatch.group(0), 
                data[rmatch.end():], self)
                
    def __repr__(self):
        return '%s %s' % (self.type.__class__.__name__, self.regex)

    def on_err(self):
        default_msgerr = 'Expected:%s' % self.children
        print(default_msgerr)

