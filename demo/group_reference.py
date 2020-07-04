from crocs.regex import Pattern, Group, X, Include, ZeroOrMore, Repeat, Seq

e0 = Group('a')
e1 = ZeroOrMore(e0)
e2 = Pattern(e0, 'b', e0)
print(e2.mkregex())
e2.test()
