import unittest
from crocs.regex import Include, Exclude, Any, OneOrZero, \
OneOrMore, Group, ConsumeNext, ConsumeBack, X, Join, Seq, Repeat,\
NamedGroup, Ask
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
        e0 = Include('x', 'y')
        e1 = Include('m', 'n')

        e2 = Any(e0, e1)
        regstr = e2.mkregex()

        self.assertEqual(regstr, '[xy]|[mn]')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        e0 = Include('x', 'y')
        e1 = Include('m', 'n')

        e2 = Any(e0, e1)
        e3 = OneOrMore(e2)
        regstr = e3.mkregex()
        self.assertEqual(regstr, '([xy]|[mn])+')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        e0 = Include('x', 'y')
        e1 = Include('m', 'n')
        e2 = Include('a', Seq('0', '9'), 'b')

        e3 = Any(e0, e1, e2)
        e4 = OneOrZero(e3)
        regstr = e4.mkregex()
        self.assertEqual(regstr, '([xy]|[mn]|[a0-9b])?')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        e0 = Include('%', '#')
        e1 = Include('c', Seq('a', 'd'), Seq('0', '5'), 'd')
        e2 = Include('a', Seq('0', '9'), 'b')

        e3 = Any(e0, e1, e2)
        e4 = Repeat(e3, 3, 8)
        regstr = e4.mkregex()
        self.assertEqual(regstr, '([%\\#]|[ca-d0-5d]|[a0-9b]){3,8}')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test5(self):
        e0 = Include('a', 'b')
        e1 = Include('[a-b]')
        e2 = Group(Any(e0, e1))

        regstr = e2.mkregex()
        self.assertEqual(regstr, '([ab]|[\[a\-b\]])')

        yregex = xmake('([ab]|[\[a\-b\]])')
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), '([ab]|[\[a-b\]])')

    def test6(self):
        e0 = Include('a', 'b')
        e1 = NamedGroup('alpha', Any(e0, 'bar'))
        e2 = Any(e0, e1)

        regstr = e2.mkregex()
        self.assertEqual(regstr, '[ab]|(?P<alpha>[ab]|bar)')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test7(self):
        e0 = Include(Seq('a', 'z'))
        e1 = Include(Seq('0', '9'))
        e2 = Group(e0, e1)
        e3 = Group(e1, e0)
        e4 = Group(Any(e2, e3))

        regstr = e4.mkregex()
        self.assertEqual(regstr, '(([a-z][0-9])|([0-9][a-z]))')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test8(self):
        e0 = Include(Seq('a', 'z'))
        e1 = Group('0', e0, '9')
        e2 = Ask(e1)
        e3 = Group(e2, 'm', e1)
        e4 = Repeat(e3, 2, 4)

        regstr = e4.mkregex()

        # The resulting structure should be serialized
        # to an invalid regex.
        with self.assertRaises(re.error):
            e4.test()

        self.assertEqual(regstr, r'((0[a-z]9)*m\1){2,4}')
        yregex = xmake(regstr)

        with self.assertRaises(re.error):
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
        e0 = Include(Seq('a', 'z'))
        e1 = Exclude(Seq('1', '9'))

        e2 = Group(e0, e1)
        e3 = Join(e0, e1, e2, e2, e2)

        regstr = e3.mkregex()

        self.assertEqual(regstr, r'[a-z][^1-9]([a-z][^1-9])\1\1')
        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        e0 = Exclude(Seq('a', 'z'))
        e1 = Ask(e0)

        e2 = Group(e0, e1)
        e3 = Group(e2, e2, e2)
        e4 = Group(e3, e3, e3)

        regstr = e4.mkregex()

        self.assertEqual(regstr, r'((([^a-z][^a-z]*)\1\1)\2\2)')
        yregex = xmake(regstr)

        with self.assertRaises(re.error):
            yregex.test()

        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        e0 = Exclude(Seq('a', 'z'))
        e1 = OneOrMore(e0)

        e2 = Group(e0, e1)
        e3 = Group(e2, e2, e2)
        e4 = Group(e3, e3, e3)

        regstr = e4.mkregex()

        self.assertEqual(regstr, r'((([^a-z][^a-z]+)\1\1)\2\2)')
        yregex = xmake(regstr)

        with self.assertRaises(re.error):
            yregex.test()
        yregex.hits()

        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        e0 = Exclude(Seq('a', 'z'))
        e1 = OneOrZero(e0)

        e2 = Group(e0, e1)
        e3 = Group(e2, e2, e2)
        e4 = Any(e2, e3)

        regstr = e4.mkregex()
        self.assertEqual(regstr, r'([^a-z][^a-z]?)|(\1\1\1)')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test5(self):
        e0 = Exclude(Seq('a', 'z'))
        e1 = X()

        e2 = Group(e0, e1)
        e3 = Group(e1, e2, e2, e2, e0, e1)
        e4 = Any(e2, e3, e2, e3, e0, e1, e2, e3, e2)
        e5 = Repeat(e4, 1, 4)

        regstr = e5.mkregex()
        yregex = xmake(regstr)

        # It has to fail because Repeat add a group around
        # Any otherwise:
        #     e = Repeat(Any('a', 'b'))
        # Would serialize to 'a|b{0,}' which is not
        # what is often intended nor logically in the context.
        with self.assertRaises(re.error):
            yregex.test()

        # Even failing above it should work too.
        yregex.hits()

        # Eacc should be capable of reading back the 
        # serialized string.
        self.assertEqual(yregex.mkregex(), regstr)

class TestAny(unittest.TestCase):
    def test0(self):
        e0 = Exclude(Seq('0', '9'))
        e1 = Include(Seq('a', 'b'))
        e2 = Any(e0, e1)
        e3 = Join(e2, e2)

        regstr = e3.mkregex()

        self.assertEqual(regstr, r'[^0-9]|[a-b][^0-9]|[a-b]')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        e0 = Exclude(Seq('0', '9'))
        e1 = OneOrZero(e0)
        e2 = Any('a', e0, e1, 'b')
        e3 = Join(e2, e2)

        regstr = e3.mkregex()

        self.assertEqual(regstr, r'a|[^0-9]|[^0-9]?|ba|[^0-9]|[^0-9]?|b')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        e0 = Include(Seq('0', '9'))
        e1 = OneOrMore(e0)
        e2 = Group(e0, e1)
        e3 = Any(e0, e1, e2)

        regstr = e3.mkregex()

        self.assertEqual(regstr, r'[0-9]|[0-9]+|([0-9][0-9]+)')

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        e0 = Include(Seq('0', '9'))
        e1 = OneOrMore(e0)
        e2 = Group(e0, e1)
        e3 = Any(e0, e1, e2)
        e4 = Any(e3, e2, e1, e0)

        regstr = e4.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test4(self):
        e0 = Include(Seq('0', '9'))
        e1 = OneOrMore(e0)
        e2 = Group(e0, e1)
        e3 = Group(e2, e2)
        e4 = Any('b', e3, 'a')

        regstr = e4.mkregex()
        self.assertEqual(regstr, r'b|(([0-9][0-9]+)\1)|a')
        yregex = xmake(regstr)
    
        # Although the serialization and the parsing
        # of it by eacc it results to equal structures
        # the regex engine doesn't allow such a ref.
        with self.assertRaises(re.error):
            yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test5(self):
        e0 = Include(Seq('0', '9'))
        e1 = X()
        e2 = Group(e0, e1)
        e3 = OneOrMore(e2)
        e4 = Any(e0, e1, e2,e2, e3)
        e5 = Group(e4, e3, e2, 'a', 'b', e3)
        e6 = Any(e0, e1, e2, e3, e4, e5)

        e7 = Join(e0, e2, e3, e4, e5, e6, 
        'somestring',  e6, e6)

        # The regex.
        # [0-9]([0-9].)\1+[0-9]|.|\1|\1|\1+([0-9]|.|\1|\1|\1+\1+\1ab\1+)[0-9]|.\
        # |\1|\1+|[0-9]|.|\1|\1|\1+|\2Fuinho\ Violento[0-9]|.|\1|\1+|[0-9]|.\
        # |\1|\1|\1+|\2[0-9]|.|\1|\1+|[0-9]|.|\1|\1|\1+|\2

        regstr = e7.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestOneOrZero(unittest.TestCase):
    def test0(self):
        e0 = Include(Seq('0', '9'))
        e1 = Any(e0, 'ahh', X())
        e2 = OneOrZero(e1)
        e3 = Group(e1, 'ee', X(), 'uu')

        regstr = e3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        e0 = Exclude(Seq('a', 'b'))
        e1 = OneOrZero(e0)
        e2 = Group(e1, 'ee', X(), 'uu')

        regstr = e2.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        e1 = OneOrZero('fooo')
        e2 = Group(e1, 'ee', X(), 'uu')
        e3 = Join(e2, 'foobar', e2, 'bar', e2)

        regstr = e2.mkregex()
        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestOneOrMore(unittest.TestCase):
    def test0(self):
        e0 = Exclude(Seq('a', 'z'))
        e1 = Any(e0, e0, 'fooo', X(), 'ooo', e0)
        e2 = OneOrMore(e1)
        e3 = Group(e1, 'ee', X(), 'uu', e2, 'oo', e1)

        regstr = e3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        e0 = Include(Seq('a', 'b'))
        e1 = OneOrMore(e0)
        e2 = Group(e0, '111', X(), X(), '222')

        regstr = e2.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        e1 = OneOrMore('fooo')
        e2 = Group(e1, '0000000', e1, e1, X(), 'uu', e1)
        e3 = Join(e1, e2, e2, 'alpha', e2, 'bar', e2)

        # The regex.
        # (fooo)+(\1+0000000\1+\1+.uu\1+)\2alpha\2bar\2

        regstr = e3.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestGroup(unittest.TestCase):
    def test0(self):
        e0 = Group(X(), 'a', 'b')
        e1 = Group(e0, 'oo')
        e2 = Group(e1, 'mm')
        e3 = Group(e2, 'uu')
        e4 = Any(e0, e1, e2, e3)
        e5 = Join(e4, e0, e1, e2, e3, e4)

        regstr = e5.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test1(self):
        e0 = Group(X(), 'a', 'b', Include('abc'))
        e1 = Group(e0, 'uuu', 'uuu', Exclude(Seq('a', 'z')))
        e2 = Group(e1, 'mm', Any(e0, e1, 'fooo'), 'uuuuu')
        e3 = Group(e2, 'uu', Repeat('hehe', 2))
        e4 = Any(e0, e1, e2, e3)
        e5 = Join(e4, e0, e1, e2, e3, e4)

        regstr = e5.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        e0 = Group(X(), 'a', 'b', Include('abc'))
        e1 = Group(e0, 'uuu', 'uuu', Exclude(Seq('a', 'z')))
        e2 = Group(e1, 'mm', Any(e0, e1, 'fooo'), 'uuuuu')
        e3 = Group(e2, 'uu', Repeat('hehe', 2))
        e4 = Any(e0, e1, e2, e3)
        e5 = NamedGroup('fooooo', e4, e3, e0, 'hheheh')
        e6 = Join(e4, e0, e1, e2, e3, e4, e5, 'ooo', e5)
        e7 = Join(e0, e1, e5, e4, e5, 'ooo', e5, X(), X())
        e8 = OneOrMore(e7)
        e9 = Join(e0, e1, e2, e3, e4, e5, e6, e7, e8)
        regstr = e9.mkregex()

        yregex = xmake(regstr)
        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestNamedGroup(unittest.TestCase):
    def test0(self):
        e0 = NamedGroup('beta', 'X', X(), 'B')
        e1 = Join('um', e0, 'dois', e0, 'tres', e0)
        
        regstr = e1.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)
        
    def test1(self):
        e0 = NamedGroup('alpha', 'X', OneOrMore(Group('a', 'b')), 'B')
        e1 = Any(e0, 'abc', X(), 'edf')
        e2 = Join(e0, e1, X(), 'foobar')
        
        regstr = e2.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test2(self):
        # Check if it works for nested named groups.
        e0 = NamedGroup('alpha', 'X', OneOrMore(Group('a', 'b')), 'B')
        e1 = NamedGroup('beta', 'Lets be overmen.')
        e2 = NamedGroup('gamma', OneOrZero(e1), 'rs', OneOrMore('rs'))
        e3 = NamedGroup('delta', e0, e1, e2, 'hoho')
        e4 = Join(e0, e1, e0, e1, e2, e3)
        
        regstr = e4.mkregex()

        # The regex.
        # (?P<alpha>X(ab)+B)(?P<beta>Lets\ be\ overmen\.)(?P=alpha)(?P=beta)\
        # (?P<gamma>(?P=beta)?rs(rs)+)(?P<delta>(?P=alpha)(?P=beta)(?P=gamma)hoho)
        # Check if eacc can build it back.
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

    def test3(self):
        e0 = NamedGroup('foobar', Repeat(Any('a', X(), 'b')))
        e1 = Any(e0, 'm', 'n', Group(e0, '12', X()))

        regstr = e1.mkregex()
        yregex = xmake(regstr)

        yregex.test()
        yregex.hits()
        self.assertEqual(yregex.mkregex(), regstr)

class TestRepeat(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestAsk(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestConsumeNext(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestConsumeBack(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestSeq(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestDot(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestJoin(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass


if __name__ == '__main__':
    unittest.main()