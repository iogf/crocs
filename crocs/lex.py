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
        self.expect = None

        # The initial state is self.expect = self 
        # and xstack empty. If it hits '' and this state
        # is not fullfilled then it is a broken doc.
        #    
        # Another possibility for a bad state it is if no token
        # is matched, in that case self.expect will tell why it failed.

    def eof(self):
        if self.xstack or self.expect:
            self.handle_err('')

    def handle_err(self, data):
        print('Crocs: Errors!') 
        print('> Expected: %s' % (self.expect if self.expect else self))

        print('> Data: %s' % repr(data))
        print('> Xstack:%s' % self.xstack)

    def init_state(self, data):
        """
        This is a map of LexChain instances. Each one fo these 
        contain a regex that is to be matched against the data.
        
        This method goes through all the regex's to match 
        at least one.

        When one of these child patterns match them may change
        the state of this LexMap instance. 

        The relevant variable that's changed it is the 
        self.expect which is what to be matched.


        This attempt to match the data against the initial state
        of this machine and its sub machines. When there is a match
        then the current state is saved for later processing.

        Note: LexMap doesn't change its own state directly. The trigger
        classes are the ones that elect a state for LexMap.

        LexMap merely offers means of managing its state by its trigger
        classes.
        """
        for ind in self.children:
            token = ind.init_state(data)
            if token:
                return token

        self.handle_err(data)
        pass

    def push(self, xnode):
        """
        This is used to switch this machine to other state.

        The xnode is also a state machine tha has to be in a specific
        state to be valid.

        """
        self.xstack.append(self.expect)
        self.expect = xnode

    def pull(self, xnode):
        """
        Pull this machine to a previous suitable state 
        which might be related to xnode machine state.
        """
        if self.xstack:
            self.expect = self.xstack.pop()

    def consume(self, data):
        """
        """

        # If self.expect is None then it is in its initial state.
        # It matches the data against its initial state.
        #
        # When self.expect is None it means none of the triggers
        # need to have special sequences coming. It is not the case of
        # LexChain that always changes its LexMap instance's state.
        #
        # When the doc is ok then all the triggers's state should be in its
        # initial value.
        if not self.expect:
            return self.init_state(data)

        # At this point the machine 
        token = self.expect.consume(data)
        if token:
            return token
        pass
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

    def push(self, index):
        """    
        This method saves the actual state of this machine onto
        self.istack. It also save the lexmap state.


        The basic idea consists of allowing other machines to change
        this machine state and having this machine state to return to its
        previous state to accomplish the job.
        """
        self.istack.append(self.index)
        self.index = index
        self.lexmap.push(self)

    def init_state(self, data):
        """    
        Attempt to match this chain at the beginning.
        When it matches then the current state is saved
        for later processing.
        """
        token = self.children[0].consume(data)

        # It saves the actual state of this machine. The self.index value
        # is the important one for restarting the process later.
        # self.push(0)
        #
        # When the parsing ends and self.index is not 0 then
        # it means the doc is not valid.
        #
        # It pushes itself to be parsed later only if there are
        # more than one rule to be matched otherwise it is already 
        # fully consumed.
        if token and len(self.children) > 1:
            self.push(1)
        return token

    def consume(self, data):
        """
        Attempt to match the self.index pattern against the data.
        If it matches it means the machine is in good state thus
        it increases self.index for a later match.

        It basically matches the current state against the pattern.
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
        When this trigger is filled it means its machine
        has to be returned to its initial state. 

        The initial state is characterized by self.index
        so it has to be None.
        """
        self.index = self.istack.pop()
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

