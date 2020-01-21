from crocs.regex import Join, Include, Seq

e = Join('x', Include(Seq('0', '9')))
e.test()
e.hits()
