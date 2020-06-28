from crocs.regex import Join, Group, X, Include, ZeroOrMore, Repeat, Seq

e0 = Group('a')
e1 = ZeroOrMore(e0)
e2 = Join(e0, 'b', e0)
print(e2.mkregex())
e2.test()
