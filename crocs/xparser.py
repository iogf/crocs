from yacc.yacc import Yacc
from crocs.grammar import RegexLexer, RegexGrammar

class XParser(Yacc):
    def __init__(self, grammar):
        super(XParser, self).__init__(grammar)
        # Normal groups refs.
        self.gref = {}

        # Named groups refs.
        self.gnref = {}

    def build(self, data):
        pass

    def r_char(self, sof, regex, eof):
        pass

    def r_dot(self, sof, regex, eof):
        pass

    def r_done(self, sof, regex, eof):
        pass
