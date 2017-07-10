from crocs import *

e = Pattern(ConsumeBack('abc', 'def', neg=True))
e.test()

