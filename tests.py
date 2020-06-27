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

class TestAny(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestOneOrZero(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestOneOrMore(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestGroup(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

class TestNamedGroup(unittest.TestCase):
    def setUp(self):
        pass

    def test0(self):
        pass

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