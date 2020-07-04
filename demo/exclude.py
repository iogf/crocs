from crocs.regex import Pattern, Include, Exclude, Seq

e = Pattern(Exclude('abc'), Include(Seq('0', '9')))
e.test()
e.hits()
