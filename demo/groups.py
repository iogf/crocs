from crocs import *

e = Pattern(Group(Exclude('abc'), 'cuca'), Times(
NamedGroup('alpha', Include('mnc'), 'done'), 4))

e.test()



