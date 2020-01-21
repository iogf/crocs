from crocs.regex import Join, Group, X

e = Join('a', Group('b', X()))
e.test()
e.hits()
