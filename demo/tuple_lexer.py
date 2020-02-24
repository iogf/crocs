"""
"""

from crocs.lexer import Lexer, LexMap, SeqNode, LexRef, LexSeq, LexNode, XSpec
from crocs.token import Num, LP, RP, Blank, Comma

class TupleTokens(XSpec):
    lexmap = LexMap()
    t_paren = LexSeq(SeqNode(r'\(', LP), LexRef(lexmap),
    SeqNode(r'\)', RP))

    t_elem = LexSeq(SeqNode(r',', Comma), LexRef(lexmap))

    t_num = LexNode(r'[0-9]+', Num)
    t_blank = LexNode(r' +', Blank)
    lexmap.add(t_paren, t_elem, t_num, t_blank)
    root = lexmap

print('Example 1')
lex = Lexer(TupleTokens)
data = '(1, 2, 3, (1, 2, 3))'
tokens = lex.feed(data)
print('Consumed:', list(tokens))