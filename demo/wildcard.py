from crocs.regex import Pattern, X

e = Pattern('a', X(), 'b')
e.test()
e.hits()

