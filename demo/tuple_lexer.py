"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexRef, LexChain
from crocs.token import Token

class ListTokens:
    lexmap = LexMap()
    LexChain(lexmap, 
    LexNode('\(', Token),
    LexRef(lexmap),
    LexNode('\)', Token))

    LexChain(lexmap, 
    LexNode(',', Token), LexRef(lexmap))

    LexChain(lexmap, LexNode('[0-9]+', Token))

    LexChain(lexmap, LexNode(' +', Token))

print('Example 1')
lex = Lexer(ListTokens.lexmap)
data = '(1, 2, 3, (1, 2, 3))'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2')
lex = Lexer(ListTokens.lexmap)
data = '(1, 2, 3, (1, 2, 3), ())'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 3')
lex = Lexer(ListTokens.lexmap)
data = '(1, 2, (), 3, (1, 2, 3), ())'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 4')
lex = Lexer(ListTokens.lexmap)
data = '(1, 2, (,1), (3, (1, 2, 3), ())'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 4')
lex = Lexer(ListTokens.lexmap)
data = '(1, 2, (), (), (1, 2), 4)'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 4')
lex = Lexer(ListTokens.lexmap)
data = '(1, (), )'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 4')
lex = Lexer(ListTokens.lexmap)
data = '(1, ), )'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))
