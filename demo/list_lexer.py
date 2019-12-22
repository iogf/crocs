"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexLink
from crocs.token import Token

class ListTokens:
    lexmap = LexMap()
    t0 = LexNode(lexmap, '\[', Token)
    t1 = LexLink(t0, lexmap)
    t2 = LexNode(t1, '\]', Token)
    t3 = LexNode(lexmap, ',', Token)

    t4 = LexNode(lexmap, '[0-9]+', Token)

    t5 = LexNode(lexmap, ' +')

print('Example 1')
lex = Lexer(ListTokens.lexmap)
data = '[]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2')
lex = Lexer(ListTokens.lexmap)
data = '[1, [2, [1,]]]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 3')
lex = Lexer(ListTokens.lexmap)
data = '[1, ss]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 4')
lex = Lexer(ListTokens.lexmap)
data = '[22,2, [, ]]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 5')
lex = Lexer(ListTokens.lexmap)
data = '[22,2, [23, 1, 4, 2], [1, [23]]]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


