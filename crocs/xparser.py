from eacc.eacc import Eacc
from eacc.lexer import Lexer
from crocs.grammar import RegexGrammar, XSetGrammar
from crocs.regex import X, Join, Group, Repeat

class XSParser(Eacc):
    def __init__(self, grammar):
        super(XSParser, self).__init__(grammar)
        self.add_handle(RegexGrammar.t_seq, self.r_seq)

    def r_done(self, start, minus, end):
        pass

    def r_seq(self, start, minus, end):
        pass

class RegexParser(Eacc):
    def __init__(self):
        super(RegexParser, self).__init__(RegexGrammar)
        # Normal groups refs.
        self.gref = {}

        # Named groups refs.
        self.gnref = {}
        # self.xsparser = XSParser(XSetGrammar)
        # self.add_handle(RegexGrammar.r_escape, self.escape)

        self.add_handle(RegexGrammar.r_group, self.group)
        self.add_handle(RegexGrammar.r_dot, self.dot)
        self.add_handle(RegexGrammar.r_times0, self.times0)
        self.add_handle(RegexGrammar.r_times1, self.times1)
        self.add_handle(RegexGrammar.r_times2, self.times2)
        self.add_handle(RegexGrammar.r_times3, self.times3)
        self.add_handle(RegexGrammar.r_times4, self.times4)
        self.add_handle(RegexGrammar.r_times5, self.times5)
        self.add_handle(RegexGrammar.r_times6, self.times6)
        self.add_handle(RegexGrammar.r_set, self.include)

        self.add_handle(RegexGrammar.r_char, self.char)
        self.add_handle(RegexGrammar.r_join, self.join)

        self.add_handle(RegexGrammar.r_done, self.done)

    def build(self, tokens):
        ptree = super(RegexParser, self).build(tokens)
        return list(ptree)

    def group(self, lp, regex, rp):
        e = Group(regex.val())
        return e

    def escape(self, escape, char):
        pass

    def include(self, escape, char):
        pass

    def dot(self, dot):
        x = X()
        return x

    def times0(self, regex, lbr, min, comma, max, rbr):
        e = Repeat(regex.val(), int(min.val()), int(max.val()))
        return e

    def times1(self, regex, lbr, num, rbr):
        e = Repeat(regex.val(), int(num.val()), int(num.val()))
        return e

    def times2(self, lbr, min, comma, rbr):
        pass

    def times3(self, lbr, comma, max, rbr):
        pass

    def times4(self, regex, mul):
        e = Repeat(regex.val())
        return e

    def times5(self, regex, question):
        e = Repeat(regex.val(), 0, 1)
        return e

    def times6(self, regex, question):
        e = Repeat(regex.val(), 1)
        return e

    def set(self, lb, chars, rb):
        pass

    def char(self, char):
        return char.val()

    def join(self, regex):
        data = (ind.val() for ind in regex)
        join = Join(*data)
        return join

    def done(self, sof, regex, eof):
        ast = regex.val()
        ast.test()
        ast.hits()

