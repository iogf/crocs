from crocs.regex import Join, Any

e0 = Join(Any('alpha', 'beta'), 'gamma')
e0.test()
e0.hits()

