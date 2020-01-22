from crocs.regex import Join, ConsumeBack

e = ConsumeBack('Isaac ', 'Asimov', neg=True)
e.test()
e.hits()
