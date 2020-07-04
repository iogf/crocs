from crocs.regex import Pattern, ConsumeNext, X

e = ConsumeNext(Pattern('a', X(), 'b'), 'def')
e.test()
e.hits()

