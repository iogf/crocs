from crocs.regex import Join, ConsumeNext, X

e = ConsumeNext(Join('a', X(), 'b'), 'def')
e.test()
e.hits()

