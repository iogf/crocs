from crocs.regex import Join, Include, Exclude, Seq

e = Join(Exclude('abc'), Include(Seq('0', '9')))
e.test()
e.hits()
