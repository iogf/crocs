from eacc.eacc import Eacc
from eacc.lexer import Lexer
from crocs.grammar import RegexGrammar, IncludeGrammar, ExcludeGrammar
from crocs.regex import X, Join, Group, Repeat, Seq, Include, Exclude

class IncludeSet(Eacc):
    def __init__(self):
        super(IncludeSet, self).__init__(IncludeGrammar)
        self.add_handle(IncludeGrammar.r_seq, self.seq)
        self.add_handle(IncludeGrammar.r_done, self.done)
        self.add_handle(IncludeGrammar.r_char, self.char)

    def seq(self, start, minus, end):
        seq = Seq(start.val(), end.val())
        return seq

    def char(self, char):
        return char.val()

    def done(self, sof, regex, eof):
        data = (ind.val() for ind in regex)
        include = Include(*data)
        return include

class ExcludeSet(Eacc):
    def __init__(self):
        super(ExcludeSet, self).__init__(ExcludeGrammar)

        self.add_handle(ExcludeGrammar.r_seq, self.seq)
        self.add_handle(ExcludeGrammar.r_char, self.char)
        self.add_handle(ExcludeGrammar.r_done, self.done)

    def seq(self, start, minus, end):
        seq = Seq(start.val(), end.val())
        return seq

    def char(self, char):
        return char.val()

    def done(self, sof, regex, eof):
        data = (ind.val() for ind in regex)
        exclude = Exclude(*data)
        return exclude

class RegexParser(Eacc):
    def __init__(self):
        super(RegexParser, self).__init__(RegexGrammar)
        # Normal groups refs.
        self.gref = {}

        # Named groups refs.
        self.gnref = {}
        self.include_set = IncludeSet()
        self.exclude_set = ExcludeSet()

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
        self.add_handle(RegexGrammar.r_include, self.include)
        self.add_handle(RegexGrammar.r_exclude, self.exclude)

        self.add_handle(RegexGrammar.r_char, self.char)

        self.add_handle(RegexGrammar.r_done, self.done)

    def build(self, tokens):
        ptree = super(RegexParser, self).build(tokens)
        return list(ptree)

    def group(self, lp, regex, rp):
        data = (ind.val() for ind in regex)
        e    = Group(*data)
        return e

    def escape(self, escape, char):
        pass

    def include(self, lb, chars, rb):
        ptree = self.include_set.build(chars)
        ptree = list(ptree)[-1]
        return ptree.val()

    def exclude(self, lb, circumflex, chars, rb):
        ptree = self.exclude_set.build(chars)
        ptree = list(ptree)[-1]
        return ptree.val()

    def dot(self, dot):
        x = X()
        return x

    def times0(self, regex, lbr, min, comma, max, rbr):
        e = Repeat(regex.val(), int(min.val()), int(max.val()))
        return e

    def times1(self, regex, lbr, num, rbr):
        e = Repeat(regex.val(), int(num.val()), int(num.val()))
        return e

    def times2(self, regex, lbr, min, comma, rbr):
        e = Repeat(regex.val(), int(min.val()))
        return e

    def times3(self, regex, lbr, comma, max, rbr):
        e = Repeat(regex.val(), max=int(max.val()))
        return e

    def times4(self, regex, mul):
        e = Repeat(regex.val())
        return e

    def times5(self, regex, question):
        e = Repeat(regex.val(), 0, 1)
        return e

    def times6(self, regex, question):
        e = Repeat(regex.val(), 1)
        return e

    def char(self, char):
        return char.val()

    def done(self, sof, regex, eof):
        data = (ind.val() for ind in regex)
        join = Join(*data)
        join.test()
        join.hits()
        return join

