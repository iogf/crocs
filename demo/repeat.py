from crocs.regex import Pattern, Repeat

e = Pattern('a', Repeat('b'), Repeat('cd'))
e.test()
e.hits()