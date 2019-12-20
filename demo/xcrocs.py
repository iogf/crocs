from crocs.regex import *

g = Group('X',Repeat(Include(Seq('0', '9')), 1, 4))
e = Join(g, Repeat(Include(Seq('a', 'z')), 1, 3), g)

e.test()
e.hits()

# It will consume abc only if it is not followed by aaa.
c = Include('aum')
e1 = Join(ConsumeBack('abc', Repeat(c, 3, 6), neg=True))
e1.test()
e1.hits()

c = Include('aum')
e2 = Join(ConsumeNext('abc', Repeat(c, 3, 6), neg=True))
e2.test()
e1.hits()


# Example with conditions.
e = Join(ConsumeNext('abc', 'def'))
e.test()

p0 = Repeat(Include('a', 'z'), 1, 10)
p1 = Any('alpha', 'beta', p0)

p1.test()
p1.hits()

e = Join(Exclude('abc'), Include('xv'))
e.test()

e = Join(ConsumeNext('abc', 'def', neg=True))
e.test()

e = Join(Repeat(Exclude(Seq('a', 'c')), 3), Include(Seq('m', 'z')), '-123')
e.test()

e = Join(ConsumeBack('abc', 'def'))
e.test()

e = Join('alpha', Repeat(X(), 3))
e.test()

e = Join(Repeat(X(), 1), 'cde', Repeat(Group('bum'), 3))
e.test()

x = Seq('0', '9')
e0 = Join('alpha-', Repeat(Include(x), 1, 4))
print('Regex:', e0.to_regex())

e0 = Join(Repeat(X(), 1))
e0.test()

e = Join(Group(Exclude('abc'), 'cuca'))
e.test()

e = Join(Repeat(X(), 3, 5))
e.test()

e = Join(Repeat(Include(Seq('a', 'z')), 5), '-',
NamedGroup('num', Include(Seq('0', '9'))))
e.test()

e0 = Join(ConsumeBack('abc', 'def', neg=True))
e0.test()
