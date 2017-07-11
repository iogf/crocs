from crocs import *

g = Group('X',Times(Include(Seq('0', '9')), 1, 4))
e = Pattern(g, Times(Include(Seq('a', 'z')), 1, 3), g)

e.test()
e.hits()

