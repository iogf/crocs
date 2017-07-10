from crocs import *

e = Pattern(ConsumeNext('abc', 'def', neg=False))
e.test()



