from crocs.lex import Lexer, LexMap, LexNode
from crocs.token import Token

lexmap = LexMap()
t0 = LexNode(lexmap, b'\"', Token)
t1 = LexNode(t0, b'[^\"]+', Token)
t2 = LexNode(t1, b'\"', Token)
t3 = LexNode(lexmap, b' +')
t4 = LexNode(lexmap, b'for', Token)
lex = Lexer(lexmap)

data = b'for "abcd for it" for "str for string" for "heheh" for'
lex.feed(data)
print(list(lex.run()))

print('-' * 50)
data = b'for "abc" for this "efg" for'
lex.feed(data)
print(list(lex.run()))
