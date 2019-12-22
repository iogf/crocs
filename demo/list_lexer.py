"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexLink
from crocs.token import Token

class ListTokens:
    lexmap = LexMap()
    t0 = LexNode(lexmap, '\[', Token)
    t1 = LexLink(t0, lexmap)
    t2 = LexNode(t1, '\]', Token)

    t3 = LexNode(lexmap, '[0-9]+', Token)
    t4 = LexNode(lexmap, ',', Token)

    t5 = LexNode(lexmap, ' +')

print('Example 1')
lex = Lexer(ListTokens.lexmap)
data = '[1, 2, [3, 5]]'
lex.feed(data)
tokens = lex.run()
print(list(tokens))

print('Example 2')
lex = Lexer(ListTokens.lexmap)
data = '[1, [2, [1, ]] abc'
lex.feed(data)
tokens = lex.run()
print(list(tokens))








