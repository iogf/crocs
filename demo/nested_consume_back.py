from crocs.regex import Pattern, ConsumeBack, X

e = ConsumeBack(ConsumeBack(Pattern('a', X(), 'b'), 'def'), 'def')
e.test()
e.hits()

