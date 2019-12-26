"""
"""

from crocs.yacc import Lexer, LexMap, SeqNode, LexSeq
from crocs.token import Token

class WordTokens:
    lexmap = LexMap()
    LexSeq(lexmap, SeqNode(r'[^0-9]+', type=Token))
    LexSeq(lexmap, SeqNode(r'2u', type=Token))
    LexSeq(lexmap, SeqNode(r'0gf', type=Token))
    LexSeq(lexmap, SeqNode(r' +', type=Token))

lex = Lexer(WordTokens.lexmap)
print('Example 1!')
data = 'Iury is known as t2u or i0gf.'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


