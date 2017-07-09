from crocs import *

e = Pattern(
    Times(Include(Seq('a', 'z')), 5), '-',
    NamedGroup('num', Include(Seq('0', '9'))))

e.test()


