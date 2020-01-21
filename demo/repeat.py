from crocs.regex import Join, Repeat

e = Join('a', Repeat('b'), Repeat('cd'))
e.test()
e.hits()