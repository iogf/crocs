from crocs import *

e = Pattern(Times(X(), 3), Times(Include('abc'), 3))

print 'Regex:', e
print 'Input:', e.valid_data()


