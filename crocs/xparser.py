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

    def r_dot(self, sof, regex, eof):
        pass

    def r_times0(self, lbr, min, comma, max, rbr):
        pass

    def r_times1(self, lbr, num, rbr):
        pass

    def r_times2(self, lbr, min, comma, rbr):
        pass

    def r_times3(self, lbr, comma, max, rbr):
        pass

    def r_times4(self, regex, mul):
        pass

    def r_times5(self, regex, question):
        pass

    def r_seq(self, start, minus, end):
        pass

    def r_set(self, lb, regex, rb):
        pass

    def r_char(self, sof, regex, eof):
        pass

    def r_done(self, sof, regex, eof):
        pass
