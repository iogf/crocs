"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexChain
from crocs.token import Token

class WordTokens:
    lexmap = LexMap()
    LexChain(lexmap, LexNode('1', type=Token),
    LexNode('2', type=Token),
    LexNode('3', type=Token))

    LexChain(lexmap, LexNode('[0-9]', type=Token))

lex = Lexer(WordTokens.lexmap)

print('Example 1!')
data = '74830349'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2!')
data = '748303149'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2!')
data = '74830312349'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))




