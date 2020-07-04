from crocs.regex import Pattern, ConsumeBack

e = ConsumeBack('Isaac ', 'Asimov', neg=True)
e.test()
e.hits()
