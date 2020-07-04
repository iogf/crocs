from crocs.regex import Pattern, NamedGroup, X

e0 = NamedGroup('beta', 'X', X(), 'B')
e1 = Pattern('um', e0, 'dois', e0, 'tres', e0)

e1.test()
e1.hits()