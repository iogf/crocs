from crocs import I, G, E, T, P, S

e = P('alpha', G(T(I(S('1', '5')), 1, 5)), 'beta')
e.test()
e.hits()
