from crocs import *

e = Pattern('alpha', Times(X(), 3), Times('2', 3), Times(Include('abc'), 3))

e.test()

