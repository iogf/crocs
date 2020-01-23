from crocs.regex import Join, ConsumeNext

e = ConsumeNext(ConsumeNext('abc', 'def', neg=True), 'def')
e.test()
e.hits()
