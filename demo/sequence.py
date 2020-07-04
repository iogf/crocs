from crocs.regex import Pattern, Include, Seq

e = Pattern('x', Include(Seq('0', '9')))
e.test()
e.hits()
