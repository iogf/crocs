from crocs import *

p0 = Times(Include('a', 'z'), 1, 10)
p1 = Any('alpha', 'beta', p0)

p1.test()
p1.hits()




