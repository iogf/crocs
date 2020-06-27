from crocs.regex import Join, NamedGroup, X
e = Join('x', NamedGroup('foo', X()))
e.test()
e.hits()