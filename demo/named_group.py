from crocs.regex import Join, NamedGroup, X

e0 = NamedGroup('beta', 'X', X(), 'B')
e1 = Join('um', e0, 'dois', e0, 'tres', e0)

e1.test()
e1.hits()