"""
"""

from crocs.lexer import Lexer, LexMap, SeqNode, LexRef, LexSeq, LexNode, XSpec
from crocs.token import Token

class TupleTokens(XSpec):
    lexmap = LexMap()
    LexSeq(lexmap, 
    SeqNode(r'\(', Token),
    LexRef(lexmap),
    SeqNode(r'\)', Token))

    LexSeq(lexmap, 
    SeqNode(r',', Token), LexRef(lexmap))

    LexNode(lexmap, r'[0-9]+', Token)
    LexNode(lexmap, r' +', Token)
    root = lexmap

print('Example 1')
lex = Lexer(TupleTokens)
data = '(1, 2, 3, (1, 2, 3))'
tokens = lex.feed(data)
print('Consumed:', list(tokens))