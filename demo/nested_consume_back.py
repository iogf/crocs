from crocs.regex import Join, ConsumeBack, X

e = ConsumeBack(ConsumeBack(Join('a', X(), 'b'), 'def'), 'def')
e.test()
e.hits()

