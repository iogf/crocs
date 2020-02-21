"""
"""

from crocs.lexer import Lexer, LexMap, LexSeq, LexNode, SeqNode, XSpec
from crocs.token import Token

class StringTokens(XSpec):
    lexmap = LexMap()

    LexSeq(lexmap, 
    SeqNode(r'\"', Token),
    SeqNode(r'[^\"]+', Token),
    SeqNode(r'\"', Token))

    LexNode(lexmap, r' +', type=Token)
    root = lexmap

lex = Lexer(StringTokens)
print('Example 1!')
data = '" This will"       "rock!"     "For sure!"'
tokens = lex.feed(data)
print('Consumed:', list(tokens))


