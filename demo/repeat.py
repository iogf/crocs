from crocs.regex import Pattern, Repeat, Group

e = Pattern('a', Repeat('b'), Repeat(Group('cd')))
e.test()
e.hits()