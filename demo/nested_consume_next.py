from crocs.regex import Pattern, ConsumeNext

e = ConsumeNext(ConsumeNext('abc', 'def', neg=True), 'def')
e.test()
e.hits()
