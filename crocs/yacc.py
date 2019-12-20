from crocs.lex import XNode

class Grammar(XNode):
    pass

class SeqMap(XNode):
    """
    """

    def __init__(self, grammar, type=None):
        """
        The grammar parameter specifies the grammar this node rule
        belongs to.

        A SeqMap object may have an action associated with. 
        When such an action is executed it produces a structure
        that has a type.

        There may exist rules in the grammar that depend on the such
        a value type to be trigged. 

        """

        pass

class TokNode(XNode):
    def __init__(self, grammar):
        pass

class TokChain(XNode):
    def __init__(self, grammar, *args):
        pass
    pass

class Yacc:
    def __init__(self, grammar):
        self.grammar = grammar
        self.rstack = []

        # Last rule that was valid.
        self.lnode = None

    def build(self, data):
        pass

    def skip(self):
        pass

    def next(self):
        pass