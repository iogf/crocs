"""
The approach consists of building regex patterns using the python classes
then serializing to a raw regex string. 

The resulting regex string is parsed by Eacc and a similar structure is built
using the same previous classes it is serialized to a raw regex then checked against the 
initial regex string.

There are tests that build the pythonic structure from a raw string
then it is serialized back and tested against the initial regex string.

This approach should be enough to make sure both crocs regex classes and
regex grammar are working. 

When a regex AST is built it is serialized, possible matches are generated
and matched against its serialized regex string. It makes sure that
the serialized regex string is valid.

Some generated hits for patterns may be too long and slow down the tests considerably.

"""

import unittest
from crocs.regex import Include, Exclude, Any, OneOrZero, \
OneOrMore, Group, ConsumeNext, ConsumeBack, X, Join, Seq, Repeat,\
NamedGroup, ZeroOrMore
from crocs.xparser import xmake
from eacc.lexer import Lexer, LexError
import re

class TestInclude(unittest.TestCase):
    def test0(self):
        e = Include('a', 'b', 'c')

        regstr = e.mkregex()
        self.assertEqual(regstr, '[abc]')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = Include('x', 'y')
        expr1 = Include('m', 'n')

        expr2 = Any(expr0, expr1)
        regstr = expr2.mkregex()

        self.assertEqual(regstr, '[xy]|[mn]')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        expr0 = Include('x', 'y')
        expr1 = Include('m', 'n')

        expr2 = Any(expr0, expr1)
        expr3 = OneOrMore(expr2, wrap=True)
        regstr = expr3.mkregex()
        self.assertEqual(regstr, '([xy]|[mn])+')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        expr0 = Include('x', 'y')
        expr1 = Include('m', 'n')
        expr2 = Include('a', Seq('0', '9'), 'b')

        expr3 = Any(expr0, expr1, expr2)
        expr4 = OneOrZero(expr3, wrap=True)
        regstr = expr4.mkregex()
        self.assertEqual(regstr, '([xy]|[mn]|[a0-9b])?')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        expr0 = Include('%', '#')
        expr1 = Include('c', Seq('a', 'd'), Seq('0', '5'), 'd')
        expr2 = Include('a', Seq('0', '9'), 'b')

        expr3 = Any(expr0, expr1, expr2)
        expr4 = Repeat(expr3, 3, 8, wrap=True)
        regstr = expr4.mkregex()
        self.assertEqual(regstr, '([%\\#]|[ca-d0-5d]|[a0-9b]){3,8}')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test5(self):
        expr0 = Include('a', 'b')
        expr1 = Include('[a-b]')
        expr2 = Group(Any(expr0, expr1))

        regstr = expr2.mkregex()
        self.assertEqual(regstr, '([ab]|[\[a\-b\]])')

        yregex = xmake('([ab]|[\[a\-b\]])')
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), '([ab]|[\[a-b\]])')

    def test6(self):
        expr0 = Include('a', 'b')
        expr1 = NamedGroup('alpha', Any(expr0, 'bar'))
        expr2 = Any(expr0, expr1)

        regstr = expr2.mkregex()
        self.assertEqual(regstr, '[ab]|(?P<alpha>[ab]|bar)')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test7(self):
        expr0 = Include(Seq('a', 'z'))
        expr1 = Include(Seq('0', '9'))
        expr2 = Group(expr0, expr1)
        expr3 = Group(expr1, expr0)
        expr4 = Group(Any(expr2, expr3))

        regstr = expr4.mkregex()
        self.assertEqual(regstr, '(([a-z][0-9])|([0-9][a-z]))')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test8(self):
        expr0 = Include(Seq('a', 'z'))
        expr1 = Group('0', expr0, '9')
        expr2 = ZeroOrMore(expr1)
        expr3 = Group(expr2, 'm', expr1)
        expr4 = Repeat(expr3, 2, 4)

        regstr = expr4.mkregex()

        expr4.test()

        yregex = xmake(regstr)

        yregex.test()

        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

class TestExclude(unittest.TestCase):
    def test0(self):
        e = Exclude(Seq('a', 'z'))

        regstr = e.mkregex()

        self.assertEqual(regstr, '[^a-z]')
        yregex = xmake(regstr)
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = Include(Seq('a', 'z'))
        expr1 = Exclude(Seq('1', '9'))

        expr2 = Group(expr0, expr1)
        expr3 = Join(expr0, expr1, expr2, expr2, expr2)

        regstr = expr3.mkregex()

        # self.assertEqual(regstr, r'[a-z][^1-9]([a-z][^1-9])\1\1')
        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        expr0 = Exclude(Seq('a', 'z'))
        expr1 = ZeroOrMore(expr0)

        expr2 = Group(expr0, expr1)
        expr3 = Group(expr2, expr2, expr2)
        expr4 = Group(expr3, expr3, expr3)

        regstr = expr4.mkregex()

        # self.assertEqual(regstr, r'((([^a-z][^a-z]*)\1\1)\1\1)')
        yregex = xmake(regstr)

        yregex.test()

        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        expr0 = Exclude(Seq('a', 'z'))
        expr1 = OneOrMore(expr0)

        expr2 = Group(expr0, expr1)
        expr3 = Group(expr2, expr2, expr2)
        expr4 = Group(expr3, expr3, expr3)

        regstr = expr4.mkregex()
        # **
        print(regstr)
        # self.assertEqual(regstr, r'((([^a-z][^a-z]+)\1\1)\1\1)')
        # yregex = xmake(regstr)
        # yregex.test()
        # self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        expr0 = Exclude(Seq('a', 'z'))
        expr1 = OneOrZero(expr0)

        expr2 = Group(expr0, expr1)
        expr3 = Group(expr2, expr2, expr2)
        expr4 = Any(expr2, expr3)

        regstr = expr4.mkregex()
        # self.assertEqual(regstr, r'([^a-z][^a-z]?)|(\1\1\1)')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestAny(unittest.TestCase):
    def test0(self):
        expr0 = Exclude(Seq('0', '9'))
        expr1 = Include(Seq('a', 'b'))
        expr2 = Any(expr0, expr1)
        expr3 = Join(expr2, expr2)

        regstr = expr3.mkregex()

        self.assertEqual(regstr, r'[^0-9]|[a-b][^0-9]|[a-b]')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = Exclude(Seq('0', '9'))
        expr1 = OneOrZero(expr0)
        expr2 = Any('a', expr0, expr1, 'b')
        expr3 = Join(expr2, expr2)

        regstr = expr3.mkregex()

        self.assertEqual(regstr, r'a|[^0-9]|[^0-9]?|ba|[^0-9]|[^0-9]?|b')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = OneOrMore(expr0)
        expr2 = Group(expr0, expr1)
        expr3 = Any(expr0, expr1, expr2)

        regstr = expr3.mkregex()

        self.assertEqual(regstr, r'[0-9]|[0-9]+|([0-9][0-9]+)')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = OneOrMore(expr0)
        expr2 = Group(expr0, expr1)
        expr3 = Any(expr0, expr1, expr2)
        expr4 = Any(expr3, expr2, expr1, expr0)

        regstr = expr4.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = OneOrMore(expr0)
        expr2 = Group(expr0, expr1)
        expr3 = Group(expr2, expr2)
        expr4 = Any('b', expr3, 'a')

        regstr = expr4.mkregex()
        # self.assertEqual(regstr, r'b|(([0-9][0-9]+)\1)|a')
        yregex = xmake(regstr)
    
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test5(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = X()
        expr2 = Group(expr0, expr1)
        expr3 = OneOrMore(expr2)
        expr4 = Any(expr0, expr1, expr2,expr2, expr3)
        expr5 = Group(expr4, expr3, expr2, 'a', 'b', expr3)
        expr6 = Any(expr0, expr1, expr2, expr3, expr4, expr5)

        expr7 = Join(expr0, expr2, expr3, expr4, expr5, expr6, 
        'somestring',  expr6, expr6)

        # The regex.
        # [0-9]([0-9].)\1+[0-9]|.|\1|\1|\1+([0-9]|.|\1|\1|\1+\1+\1ab\1+)[0-9]|.\
        # |\1|\1+|[0-9]|.|\1|\1|\1+|\2Fuinho\ Violento[0-9]|.|\1|\1+|[0-9]|.\
        # |\1|\1|\1+|\2[0-9]|.|\1|\1+|[0-9]|.|\1|\1|\1+|\2

        regstr = expr7.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestOneOrZero(unittest.TestCase):
    def test0(self):
        expr0 = Include(Seq('0', '9'))
        expr1 = Any(expr0, 'ahh', X())
        expr2 = OneOrZero(expr1)
        expr3 = Group(expr1, 'ee', X(), 'uu')

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = Exclude(Seq('a', 'b'))
        expr1 = OneOrZero(expr0)
        expr2 = Group(expr1, 'ee', X(), 'uu')

        regstr = expr2.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        expr1 = OneOrZero('fooo')
        expr2 = Group(expr1, 'ee', X(), 'uu')
        expr3 = Join(expr2, 'foobar', expr2, 'bar', expr2)

        regstr = expr2.mkregex()
        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestOneOrMore(unittest.TestCase):
    def test0(self):
        expr0 = Exclude(Seq('a', 'z'))
        expr1 = Any(expr0, expr0, 'fooo', X(), 'ooo', expr0)
        expr2 = OneOrMore(expr1)
        expr3 = Group(expr1, 'ee', X(), 'uu', expr2, 'oo', expr1)

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = Include(Seq('a', 'b'))
        expr1 = OneOrMore(expr0)
        expr2 = Group(expr0, '111', X(), X(), '222')

        regstr = expr2.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        expr1 = OneOrMore('fooo')
        expr2 = Group(expr1, '0000000', expr1, expr1, X(), 'uu', expr1)
        expr3 = Join(expr1, expr2, expr2, 'alpha', expr2, 'bar', expr2)

        # The regex.
        # (fooo)+(\1+0000000\1+\1+.uu\1+)\2alpha\2bar\2

        regstr = expr3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestGroup(unittest.TestCase):
    def test0(self):
        expr0 = Group(X(), 'a', 'b')
        expr1 = Group(expr0, 'oo')
        expr2 = Group(expr1, 'mm')
        expr3 = Group(expr2, 'uu')
        expr4 = Any(expr0, expr1, expr2, expr3)
        expr5 = Join(expr4, expr0, expr1, expr2, expr3, expr4)

        regstr = expr5.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = Group(X(), 'a', 'b', Include('abc'))
        expr1 = Group(expr0, 'uuu', 'uuu', Exclude(Seq('a', 'z')))
        expr2 = Group(expr1, 'mm', Join(expr0, expr1, 'fooo'), 'uuuuu')

        expr3 = Group(expr2, 'uu')
        expr4 = Join(expr0, expr1, expr2, expr3)
        expr5 = Join(expr4, expr0, expr1, expr2, expr3, expr4)

        regstr = expr5.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        expr0 = Group('a')
        expr1 = Group('c', Group(expr0, 'd'))
        expr2 = Group(expr1, 'e')
        expr3 = Join(expr0, expr1, expr2)

        regstr = expr3.mkregex()
        yregex = xmake(regstr)
        expr3.test()

        yregex.hits()
        yregex.test()
        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        expr0 = Group('abc')
        expr1 = Group(expr0, 'efg')
        expr2 = Group(expr0, expr1)
        regstr = expr2.mkregex()
        yregex = xmake(regstr)

        yregex.test()

        # Eacc should be capable of reading back the 
        # serialized string.
        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        expr0 = Group('ab')
        expr1 = Group(expr0, expr0)
        regstr = expr1.mkregex()
        print(regstr)
        yregex = xmake(regstr)
        print('yRegex:', yregex)
        # yregex.test()
        # self.assertEqual(yregex.mkregex(), regstr)

class TestNamedGroup(unittest.TestCase):
    def test0(self):
        expr0 = NamedGroup('beta', 'X', X(), 'B')
        expr1 = Join('um', expr0, 'dois', expr0, 'tres', expr0)
        
        regstr = expr1.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)
        
    def test1(self):
        expr0 = NamedGroup('alpha', 'X', OneOrMore(Group('a', 'b')), 'B')
        expr1 = Any(expr0, 'abc', X(), 'edf')
        expr2 = Join(expr0, expr1, X(), 'foobar')
        
        regstr = expr2.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        # Check if it works for nested named groups.
        expr0 = NamedGroup('alpha', 'X', OneOrMore(Group('a', 'b')), 'B')
        expr1 = NamedGroup('beta', 'Lets be overmen.')
        expr2 = NamedGroup('gamma', OneOrZero(expr1), 'rs', OneOrMore('rs'))

        expr3 = NamedGroup('delta', expr0, expr1, expr2, 'hoho')
        expr4 = Join(expr0, expr1, expr0, expr1, expr2, expr3)
        
        regstr = expr4.mkregex()

        # The regex.
        # (?P<alpha>X(ab)+B)(?P<beta>Lets\ be\ overmen\.)(?P=alpha)(?P=beta)\
        # (?P<gamma>(?P=beta)?rs(rs)+)(?P<delta>(?P=alpha)(?P=beta)(?P=gamma)hoho)
        # Check if eacc can build it back.
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        expr0 = NamedGroup('foobar', Repeat(Any('a', X(), 'b')))
        expr1 = Any(expr0, 'm', 'n', Group(expr0, '12', X()))

        regstr = expr1.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestRepeat(unittest.TestCase):
    def test0(self):
        expr0 = NamedGroup('oooo', Repeat(Any('a', X(), 'b')))
        expr1 = Any(expr0, 'm', 'n', Group('oooo'), Group(expr0, X(), '12oooo', X()))
        expr2 = Repeat(expr1)
        expr3 = Join(expr0, expr1, expr2)

        regstr = expr3.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = NamedGroup('oooo', Repeat(Any('a', X(), 'b')))
        expr1 = Any(expr0, 'm', 'n', Group('oooo'), Group(expr0, X(), '12oooo', X()))
        expr2 = Repeat(expr1)
        expr3 = Join(expr0, expr1, expr2)

        expr4 = Join(expr0, X(), 'ooo', X(), expr1, expr2, expr3)
        expr5 = Any(expr0, expr1, expr2, expr3, expr4)

        regstr = expr5.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        # yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)
    pass

class TestZeroOrMore(unittest.TestCase):
    def test0(self):
        expr0 = NamedGroup('alpha', Repeat(Any('a', X())))
        expr1 = Join(expr0, 'm', Group('oooo'))
        expr2 = Any(expr0, expr1)

        expr7 = ZeroOrMore(expr2)
        expr8 = Join(expr7, expr2)

        regstr = expr8.mkregex()
        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)
        
    # def test1(self):
        # expr0 = NamedGroup('a999', Repeat('a'))
# 
        # expr1 = Join(expr0, ZeroOrMore('a'), 
        # Group('oooo'), Group(expr0))
# 
        # expr2 = Repeat(expr1)
# 
        # regstr = expr2.mkregex()
        # expr2.test()
        # yregex = xmake(regstr)
        # print(yregex)
        # yregex.test()
        # yregex.hits()
        # self.assertEqual(yregex.mkregex(), regstr)

class TestConsumeNext(unittest.TestCase):
    def test0(self):
        expr0 = ConsumeNext(Group(X(), OneOrZero('alpha')), 
        Group(X(), 'bar', X()))
        expr1 = Any(expr0, X(), '123')
        regstr = expr1.mkregex()
        yregex = xmake(regstr)

        with self.assertRaises(re.error):
            yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = ConsumeNext(Group(X(), 'bar', X()), 
        Group(X(), OneOrZero('alpha')))

        expr1 = Any(expr0, X(), '123')
        expr2 = ConsumeNext(Group(X(), '579', X()), expr1)
        regstr = expr2.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        expr0 = ConsumeNext(Group(X(), 'bar', X()), 
        Group(X(), OneOrZero('alpha')))
        expr1 = Any(expr0, X(), '123')
        expr2 = ConsumeNext(Group(X(), '579', X()), expr1)

        expr3 = ConsumeBack(expr2, 
        Group(ZeroOrMore(expr2), 'aaaaa', 'bbbb', X()))

        expr3 = Join(expr3, 'aaaa', X(), OneOrZero('aaaa'))
        regstr = expr3.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestConsumeBack(unittest.TestCase):
    def test0(self):
        expr0 = ConsumeBack(Group(X(), '1010101', X()), 
        Group(X(), OneOrMore('010101')))

        expr1 = Join(expr0, 'aaaa', X(), OneOrMore('1010101'))
        expr2 = Any(expr0, expr1, X(), Group(expr1, X(), 'a'))

        regstr = expr2.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        expr0 = ConsumeBack(Group(OneOrMore(X()), 
        'aaa', X()), Group('aaa', X(), 'bbb'))

        expr1 = Any(expr0, 'aaaa', X(), OneOrMore('foobar'), X())
        expr2 = Any(expr1, expr1, X(), Group(expr1, X(), 'a'))
        expr3 = NamedGroup('xx', expr0, expr1, X(), X())
        expr4 = Join(expr0, expr1, expr2, expr3)
        regstr = expr4.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestRegexComment(unittest.TestCase):
    def test0(self):
        regstr = 'abc(?#aiosdu).+(ab)(?#asiodu\)asd)'
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        regstr = '[abc]*(?#aiosdu).+([ab]*)(?#asiodu\)[asd])'
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        regstr = '[a-z]*(?#aiosdu).+([0-9]*)(?#hehehe\)[abcde])'
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        regstr = '[a-z]*(?#aiosdu)(abc)+([0-9]+)(123)(?#....aaa\)[abcde])'
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        regstr = '[a-z]*(?#aiosdu)((ab)*)?([0-9]+)(123)(?#....aaa\)[abcde])\1aa'
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        regstr = r'''[a-z]*(?#aiosdu)((ab)*)?([0-9]+)\\
        1sdius\2(123)(?#....aaa\)[abcde])\1aa'''

        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        regstr = 'a(?#aiosdu)*b'
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

if __name__ == '__main__':
    unittest.main()