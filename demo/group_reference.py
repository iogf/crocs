from crocs.regex import Join, Group, X, Include, Ask, Repeat, Seq

e0 = Group('a')
e1 = Ask(e0)
e2 = Join(e0, 'b', e0)
print(e2.mkregex())
e2.test()
