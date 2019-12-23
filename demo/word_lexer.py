"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexChain
from crocs.token import Token

class WordTokens:
    lexmap = LexMap()
    LexChain(lexmap, LexNode('alpha', type=Token))
    LexChain(lexmap, LexNode('beta', type=Token))
    LexChain(lexmap, LexNode('gamma', type=Token))
    LexChain(lexmap, LexNode(' +', type=Token))


lex = Lexer(WordTokens.lexmap)

print('Example 1!')
data = 'alpha gamma          beta alpha'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


