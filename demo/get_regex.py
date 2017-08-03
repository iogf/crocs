from crocs import *

x = Seq('0', '9')
e0 = Pattern('alpha-', Times(Include(x), 1, 4))
print('Regex:', e0.to_regex)





