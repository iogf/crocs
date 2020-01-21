from crocs.regex import Join, X

e = Join('a', X(), 'b')
e.test()
e.hits()

