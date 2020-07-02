from eacc.eacc import Eacc
from eacc.lexer import Lexer
from crocs.grammar import RegexTokens, RegexGrammar, HClassGrammar, HClassTokens
from crocs.regex import X, Join, Group, NonCapture, NamedGroup, Repeat, ZeroOrMore, OneOrMore, \
OneOrZero, Seq, Include, Exclude, ConsumeNext, ConsumeBack, Any, NGLink, RegexComment, GLink, \
Word, NotWord, Caret, Dollar

class IncludeSet(Eacc):
    def __init__(self):
        super(IncludeSet, self).__init__(HClassGrammar)
        self.add_handle(HClassGrammar.r_seq, self.seq)
        self.add_handle(HClassGrammar.r_done, self.done)
        self.add_handle(HClassGrammar.r_char, self.char)

    def seq(self, start, minus, end):
        seq = Seq(start.val(), end.val())
        return seq

    def char(self, char):
        return char.val()

    def done(self, sof, regex, eof):
        data = (ind.val() for ind in regex)
        include = Include(*data)
        return include

class ExcludeSet(IncludeSet):
    def __init__(self):
        super(IncludeSet, self).__init__(HClassGrammar)

        self.add_handle(HClassGrammar.r_seq, self.seq)
        self.add_handle(HClassGrammar.r_char, self.char)
        self.add_handle(HClassGrammar.r_done, self.done)

    def done(self, sof, regex, eof):
        data = (ind.val() for ind in regex)
        exclude = Exclude(*data)
        return exclude

class RegexParser(Eacc):
    def __init__(self):
        super(RegexParser, self).__init__(RegexGrammar)
        self.hclass_lexer = Lexer(HClassTokens)
        self.include_set = IncludeSet()
        self.exclude_set = ExcludeSet()

        # self.add_handle(RegexGrammar.r_escape, self.escape)
        self.add_handle(RegexGrammar.r_comment, self.comment)

        self.add_handle(RegexGrammar.r_group, self.group)
        self.add_handle(RegexGrammar.r_ncapture, self.ncapture)

        self.add_handle(RegexGrammar.r_ngroup, self.ngroup)

        self.add_handle(RegexGrammar.r_dot, self.dot)
        self.add_handle(RegexGrammar.r_word, self.word)
        self.add_handle(RegexGrammar.r_nword, self.nword)

        self.add_handle(RegexGrammar.r_times0, self.times0)
        self.add_handle(RegexGrammar.r_times1, self.times1)
        self.add_handle(RegexGrammar.r_times2, self.times2)
        self.add_handle(RegexGrammar.r_times3, self.times3)
        self.add_handle(RegexGrammar.r_times4, self.times4)
        self.add_handle(RegexGrammar.r_times5, self.times5)
        self.add_handle(RegexGrammar.r_times6, self.times6)
        self.add_handle(RegexGrammar.r_times7, self.times7)
        self.add_handle(RegexGrammar.r_times8, self.times8)
        self.add_handle(RegexGrammar.r_times9, self.times9)
        self.add_handle(RegexGrammar.r_times10, self.times10)
        self.add_handle(RegexGrammar.r_times11, self.times11)
        self.add_handle(RegexGrammar.r_times12, self.times12)
        self.add_handle(RegexGrammar.r_times13, self.times13)

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
        self.add_handle(RegexGrammar.r_caret, self.caret)
        self.add_handle(RegexGrammar.r_dollar, self.dollar)

        self.add_handle(RegexGrammar.r_done, self.done)

    def build(self, tokens):
        tree = super(RegexParser, self).build(tokens)
        return list(tree)

    def word(self, escape, wsym):
        meta = Word()
        return meta

    def nword(self, escape, wsym):
        meta = NotWord()
        return meta

    def pipe(self, regex0, pipe, regex1):
        data0 = (ind.val() for ind in regex0)
        data1 = (ind.val() for ind in regex1)
        join0 = Join(*data0)
        join1 = Join(*data1)
        join2 = Any(join0, join1)
        return join2

    def group(self, lp, regex, rp):
        data  = (ind.val() for ind in regex)
        group = Group(*data)
        return group

    def ngroup(self, lp, question, gsym, lesser,  gname, greater, regex, rp):
        data = (ind.val() for ind in regex)
        group = NamedGroup(gname.val(), *data)
        return group

    def ncapture(self, lp, question, colon, regex, rp):
        data = (ind.val() for ind in regex)
        ncapture = NonCapture(*data)
        return ncapture

    def gref(self, escape, num):
        link = GLink(int(num.val()))
        return link

    def ngref(self, lp, question, gsym, equal, gname, rp):
        link = NGLink(gname.val())
        return link

    def escape(self, escape, char):
        return char.val()

    def include(self, lb, string, rb):
        tokens = self.hclass_lexer.feed(string.val())
        tree = self.include_set.build(tokens)
        tree = list(tree)[-1]
        return tree.val()

    def exclude(self, lb, caret, string, rb):
        tokens = self.hclass_lexer.feed(string.val())

        tree = self.exclude_set.build(tokens)
        tree = list(tree)[-1]
        return tree.val()

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

    def caret(self, caret):
        caret = Caret()
        return caret

    def dollar(self, caret):
        dollar = Dollar()
        return dollar

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

    def times7(self, regex, plus, question):
        """
        Greedy operators should behave alike non greedy in the context.
        Although the serialization has to be different.
        """
        repeat = OneOrMore(regex.val(), greedy=True)
        return repeat

    def times8(self, regex, ask, question):
        """
        """
        repeat = ZeroOrMore(regex.val(), greedy=True)
        return repeat

    def times9(self, regex, question0, question1):
        """
        """
        repeat = OneOrZero(regex.val(), greedy=True)
        return repeat

    def times10(self, regex, lbr, min, comma, max, rbr, question):
        repeat = Repeat(regex.val(), int(min.val()), int(max.val()), greedy=True)
        return repeat

    def times11(self, regex, lbr, min, comma, rbr, question):
        repeat = Repeat(regex.val(), int(min.val()), greedy=True)
        return repeat

    def times12(self, regex, lbr, comma, max, rbr, question):
        repeat = Repeat(regex.val(), max=int(max.val()), greedy=True)
        return repeat

    def times13(self, regex, lbr, num, rbr, question):
        repeat = Repeat(regex.val(), min=int(num.val()), 
        max=int(num.val()), greedy=True)

        return repeat

    def char(self, char):
        return char.val()

    def comment(self, lp, question, hash, comment, rp):
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
