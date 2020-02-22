"""
"""

from crocs.lexer import Lexer, LexMap, LexNode, SeqNode, LexRef, LexSeq, XSpec
from crocs.token import LB, RB, Blank, Num

class ListTokens(XSpec):
    lexmap = LexMap()
    LexSeq(lexmap, 
    SeqNode(r'\[', LB),
    LexRef(lexmap),
    SeqNode(r'\]', RB))

    LexNode(lexmap, r'[0-9]+', Num)
    LexNode(lexmap, r' +', Blank)
    root = lexmap

print('Example 1')
lex = Lexer(ListTokens)
data = '[ 1 2 [1 3 4] [2 4 [ 1 2]]]'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
