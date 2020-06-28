from eacc.eacc import Eacc
from eacc.lexer import Lexer
from crocs.grammar import RegexTokens, RegexGrammar, IncludeGrammar, ExcludeGrammar
from crocs.regex import X, Join, Group, NamedGroup, Repeat, ZeroOrMore, OneOrMore, \
OneOrZero, Seq, Include, Exclude, ConsumeNext, ConsumeBack, Any, NGLink, RegexComment

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
        self.gmap = []

        # Named groups refs.
        self.ngmap = dict()
        self.include_set = IncludeSet()
        self.exclude_set = ExcludeSet()

        # self.add_handle(RegexGrammar.r_escape, self.escape)
        self.add_handle(RegexGrammar.r_comment, self.comment)

        self.add_handle(RegexGrammar.r_group, self.group)
        self.add_handle(RegexGrammar.r_ngroup, self.ngroup)

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
        self.add_handle(RegexGrammar.r_cnext, self.cnext)
        self.add_handle(RegexGrammar.r_ncnext, self.ncnext)

        self.add_handle(RegexGrammar.r_cback, self.cback)
        self.add_handle(RegexGrammar.r_ncback, self.ncback)
        self.add_handle(RegexGrammar.r_gref, self.gref)
        self.add_handle(RegexGrammar.r_ngref, self.ngref)

        self.add_handle(RegexGrammar.r_pipe, self.pipe)
        self.add_handle(RegexGrammar.r_char, self.char)
        self.add_handle(RegexGrammar.r_done, self.done)

    def build(self, tokens):
        self.gmap.clear()
        self.ngmap.clear()

        ptree = super(RegexParser, self).build(tokens)
        return list(ptree)

    def pipe(self, regex0, pipe, regex1):
        data0 = (ind.val() for ind in regex0)
        data1 = (ind.val() for ind in regex1)
        e0 = Join(*data0)
        e1 = Join(*data1)
        e = Any(e0, e1)
        return e

    def group(self, lp, regex, rp):
        data = (ind.val() for ind in regex)
        e    = Group(*data)
        self.gmap.append(e)
        return e

    def ngroup(self, lp, question, gsym, lesser,  gname, greater, regex, rp):
        data0 = (ind.val() for ind in regex)
        e = NamedGroup(gname.val(), *data0)

        # Remember the named group.
        self.ngmap[gname.val()] = e
        return e

    def gref(self, escape, num):
        return self.gmap[int(num.val()) - 1]

    def ngref(self, lp, question, gsym, equal, gname, rp):
        e = NGLink(gname.val())
        return self.ngmap.get(gname.val(), e)

    def escape(self, escape, char):
        return char.val()

    def include(self, lb, chars, rb):
        ptree = self.include_set.build(chars)
        ptree = list(ptree)[-1]
        return ptree.val()

    def exclude(self, lb, caret, chars, rb):
        ptree = self.exclude_set.build(chars)
        ptree = list(ptree)[-1]
        return ptree.val()

    def cnext(self, lp, question, lexer, equal, regex0, rp, regex1):
        data0 = (ind.val() for ind in regex0)
        data1 = (ind.val() for ind in regex1)
        join0 = Join(*data0)
        join1 = Join(*data1)
        e = ConsumeNext(join0, join1)
        return e

    def ncnext(self, lp, question, lexer, exlam, regex0, rp, regex1):
        data0 = (ind.val() for ind in regex0)
        data1 = (ind.val() for ind in regex1)
        join0 = Join(*data0)
        join1 = Join(*data1)
        e = ConsumeNext(join0, join1, neg=True)
        return e

    def cback(self, regex0, lp, question,  equal, regex1, rp):
        data0 = (ind.val() for ind in regex0)
        data1 = (ind.val() for ind in regex1)
        join0 = Join(*data0)
        join1 = Join(*data1)
        e = ConsumeBack(join0, join1)
        return e

    def ncback(self, regex0, lp, question, exlam, regex1, rp):
        data0 = (ind.val() for ind in regex0)
        data1 = (ind.val() for ind in regex1)
        join0 = Join(*data0)
        join1 = Join(*data1)
        e = ConsumeBack(join0, join1, neg=True)
        return e

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
        e = ZeroOrMore(regex.val())
        return e

    def times5(self, regex, question):
        e = OneOrZero(regex.val())
        return e

    def times6(self, regex, question):
        e = OneOrMore(regex.val())
        return e

    def char(self, char):
        return char.val()

    def comment(self, lp, question, hash, comment, rp):
        print('Foo', lp, question, hash, comment, rp)
        return RegexComment(comment.val())

    def done(self, sof, regex, eof):
        data = (ind.val() for ind in regex)
        join = Join(*data)
        return join

def xmake(regstr):
    xlexer  = Lexer(RegexTokens)
    xparser = RegexParser()

    tokens  = xlexer.feed(regstr)
    tseq = xparser.build(tokens)
    tseq = list(tseq)
    # regtree = tseq[-1].val()
    # regtree.test()
    # regtree.hits()

    return tseq[-1].val()
