import re
import time

class XNode:
    pass

class LexConsumer:

class Lexer:
    def __init__(self, lexmap):
        """
        """
        self.lexmap = lexmap

        # Last regex node that was matched.
        self.lnode = lexmap

    def feed(self, data):
        """
        """
        offset = 0
        while data:
            state = self.lnode.consume(data)
            if state: 
                self.set_rule(state[2])
                if state[2].type: 
                     yield state[2].type(state[0])
                data = state[1]
            else:
                break

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
    def __init__(self, xnode=None, err=None):
        """
        """

        self.xnode    = xnode
        self.children = []
        if xnode:
            self.xnode.children.append(self)

    def consume(self, data):
        for ind in self.children:
            state = ind.is_valid(data)
            if state:
                return state

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
                

