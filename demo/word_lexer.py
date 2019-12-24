"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexChain
from crocs.token import Token

class WordTokens:
    lexmap = LexMap()
    LexChain(lexmap, LexNode('[^0-9]+', type=Token))
    LexChain(lexmap, LexNode('2u', type=Token))
    LexChain(lexmap, LexNode('0gf', type=Token))
    LexChain(lexmap, LexNode(' +', type=Token))

lex = Lexer(WordTokens.lexmap)
print('Example 1!')
data = 'Iury is known as t2u or i0gf.'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


