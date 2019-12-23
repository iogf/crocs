"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexLink
from crocs.token import Token

class ListTokens:
    lexmap = LexMap()
    LexChain(lexmap, 
    LexNode('\[', Token),
    LexLink(lexmap),
    LexNode(',', Token),
    LexNode('\]', Token))

    LexChain(lexmap, LexNode('[0-9]+', Token))
    LexChain(lexmap, LexNode(' +', token))

# print('Example 1')
# lex = Lexer(ListTokens.lexmap)
# data = '[]'
# lex.feed(data)
# tokens = lex.run()
# print('Consumed:', list(tokens))

# print('Example 2')
# lex = Lexer(ListTokens.lexmap)
# data = '[1, [2, [1,]]]'
# lex.feed(data)
# tokens = lex.run()
# print('Consumed:', list(tokens))
# 
# print('Example 3')
# lex = Lexer(ListTokens.lexmap)
# data = '[1, ss]'
# lex.feed(data)
# tokens = lex.run()
# print('Consumed:', list(tokens))
# 
# print('Example 4')
# lex = Lexer(ListTokens.lexmap)
# data = '[22,2, [, ]]'
# lex.feed(data)
# tokens = lex.run()
# print('Consumed:', list(tokens))

print('Example 5')
lex = Lexer(ListTokens.lexmap)
data = '[[22, 2], [1, 2]]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


