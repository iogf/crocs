from crocs import *

x = Seq('a', 'c')
e0 = Pattern(Times(x, 1))
print(repr(e0.invalid_data()))


