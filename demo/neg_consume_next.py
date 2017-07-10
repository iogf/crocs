from crocs import *

e = Pattern(ConsumeNext('abc', 'def', neg=True))
e.test()




