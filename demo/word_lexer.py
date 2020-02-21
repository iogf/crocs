"""
"""

from crocs.lexer import Lexer, LexMap, SeqNode, LexSeq, XSpec
from crocs.token import Token

class WordTokens(XSpec):
    lexmap = LexMap()
    LexSeq(lexmap, SeqNode(r'[^0-9]+', type=Token))
    LexSeq(lexmap, SeqNode(r'2u', type=Token))
    LexSeq(lexmap, SeqNode(r'0gf', type=Token))
    LexSeq(lexmap, SeqNode(r' +', type=Token))
    root = lexmap

lex = Lexer(WordTokens)
print('Example 1!')
data = 'Iury is known as t2u or i0gf.'
tokens = lex.feed(data)
print('Consumed:', list(tokens))


