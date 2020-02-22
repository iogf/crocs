"""
"""

from crocs.lexer import Lexer, LexMap, SeqNode, LexRef, LexSeq, LexNode, XSpec
from crocs.token import Num, LP, RP, Blank, Comma

class TupleTokens(XSpec):
    lexmap = LexMap()
    LexSeq(lexmap, 
    SeqNode(r'\(', LP),
    LexRef(lexmap),
    SeqNode(r'\)', RP))

    LexSeq(lexmap, 
    SeqNode(r',', Comma), LexRef(lexmap))

    LexNode(lexmap, r'[0-9]+', Num)
    LexNode(lexmap, r' +', Blank)
    root = lexmap

print('Example 1')
lex = Lexer(TupleTokens)
data = '(1, 2, 3, (1, 2, 3))'
tokens = lex.feed(data)
print('Consumed:', list(tokens))