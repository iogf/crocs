from crocs.regex import Pattern, Any

e0 = Pattern(Any('alpha', 'beta'), 'gamma')
e0.test()
e0.hits()

