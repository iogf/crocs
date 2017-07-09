from crocs import *

e = Pattern(X(), Times(Exclude('abc'), 3), Times(Include('xv'), 4))

e.test()

