from crocs.regex import Join, Include

e = Join('a', Include('bc123'))
e.test()
e.hits()


