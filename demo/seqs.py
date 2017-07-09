from crocs import *

e = Pattern(Times(Exclude(Seq('a', 'c')), 3), Include(Seq('m', 'z')), '-123')

e.test()



