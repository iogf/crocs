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
        # self.lexmap.clear()

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

        # This is a state machine. When a given LexChain
        # is trigged then the current state is saved here.
        self.xstack = []

        # The expected LexChain that has to be matched.
        # When a LexChain is trigged then its previous is saved
        # onto the self.xstack and the new one is set here.
        self.expect = self

        # The initial state is self.expect = self 
        # and xstack empty. If it hits '' and this state
        # is not fullfilled then it is a broken doc.
        #    
        # Another possibility for a bad state it is if no token
        # is matched, in that case self.expect will tell why it failed.

    def eof(self):
        if self.xstack:
            self.handle_err('')

    def handle_err(self, data):
        print('Crocs: Errors!') 
        print('> Expected: %s' % self.expect)
        print('> Data: %s' % repr(data))
        print('> Xstack:%s' % self.xstack)

    def consume_children(self, data):
        """
        This is a map of LexChain instances. Each one fo these 
        contain a regex that is to be matched against the data.
        
        This method goes through all the regex's to match 
        at least one.
        """
        for ind in self.children:
            token = ind.consume(data)
            if token:
                return token
        pass

    def push(self, xnode):
        """
        This is used to switch this machine to other state.

        The xnode is also a state machine tha has to be in a specific
        state to be valid.

        """

        self.expect = xnode

    def pull(self, xnode):
        """
        Pull this machine to a previous suitable state 
        which might be related to xnode machine state.
        """
        self.expect = self

    def consume(self, data):
        token = self.expect.consume_children(data)
        if token:
            return token
        self.handle_err(data)

    def __repr__(self):
        return '%s' % self.children

class LexChain(XNode):
    """
    This node is supposed to change its root node state.
    """
    def __init__(self, lexmap, *args):
        self.lexmap = lexmap
        self.index = 0
        self.istack = []
        self.children = []
        self.children.extend(args)

        lexmap.children.append(self)

    def consume_children(self, data):
        """    
        Attempt to match this chain at the beginning.
        """
        token = self.children[0].consume(data)

        # It changes the machine state. When data is input
        # it will attempt to match against this LexChain. 
        # 
        # If the next data doesn't fit the LexChain state rule
        # then it is a broken state machine.
        self.lexmap.push(self)
        return token
        pass

    def consume(self, data):
        """
        Attempt to match the self.index pattern against the data.
        If it matches it means the machine is in good state thus
        it increases self.index for a later match.
        """

        token = self.children[self.index].consume(data)
        self.index = self.index + 1

        # It means the chain was fully matched or the pattern failed
        # to match.
        #
        # Thus it resets its machine to its initial state for
        # matching the next pattern.

        if self.index >= len(self.children) or not token:
            self.pull()
        pass

        return token

    def pull(self):
        """
        """
        self.index = 0
        self.lexmap.pull(self)

    def __repr__(self):
        return '%s' % self.children

class LexNode(LexMap):
    def __init__(self, regex, type=Token):
        """
        """

        err1 = 'Crocs: Invalid regex value'
        assert isinstance(regex, str), err1

        super(LexNode, self).__init__()
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
        return token

    def __repr__(self):
        return '(%s, %s)' % (self.type.__name__, repr(self.regex))

class LexLink(LexMap):
    def __init__(self, xnode, lexmap):
        """
        """
    def consume(self, data):
        """
        """
    def __repr__(self):
        return '%s' % self.expect

