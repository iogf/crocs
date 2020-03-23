from yacc.yacc import Yacc
from crocs.grammar import RegexLexer, RegexGrammar

class XParser(Yacc):
    def __init__(self, grammar):
        super(XParser, self).__init__(grammar)
        # Normal groups refs.
        self.gref = {}

        # Named groups refs.
        self.gnref = {}
        self.add_handle(RegexGrammar.t_escape, self.r_escape)
        self.add_handle(RegexGrammar.t_dot, self.r_dot)
        self.add_handle(RegexGrammar.t_times0, self.r_times0)
        self.add_handle(RegexGrammar.t_times1, self.r_times1)
        self.add_handle(RegexGrammar.t_times2, self.r_times2)
        self.add_handle(RegexGrammar.t_times3, self.r_times3)
        self.add_handle(RegexGrammar.t_times4, self.r_times4)
        self.add_handle(RegexGrammar.t_times5, self.r_times5)
        self.add_handle(RegexGrammar.t_times6, self.r_times6)
        self.add_handle(RegexGrammar.t_seq, self.r_seq)
        self.add_handle(RegexGrammar.t_set, self.r_set)

        self.add_handle(RegexGrammar.t_char, self.r_char)
        self.add_handle(RegexGrammar.t_done, self.r_done)

    def build(self, data):
        pass

    def r_escape(self, escape, char):
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
