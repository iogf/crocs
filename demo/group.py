from crocs.regex import Pattern, Group, X

e = Pattern('a', Group('b', X()))
e.test()
e.hits()
