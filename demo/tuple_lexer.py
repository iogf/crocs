"""
"""

from crocs.yacc import Lexer, LexMap, SeqNode, LexRef, LexSeq, LexNode
from crocs.token import Token

class TupleTokens:
    lexmap = LexMap()
    LexSeq(lexmap, 
    SeqNode(r'\(', Token),
    LexRef(lexmap),
    SeqNode(r'\)', Token))

    LexSeq(lexmap, 
    SeqNode(r',', Token), LexRef(lexmap))

    LexNode(lexmap, r'[0-9]+', Token)
    LexNode(lexmap, r' +', Token)

print('Example 1')
lex = Lexer(TupleTokens.lexmap)
data = '(1, 2, 3, (1, 2, 3))'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2')
lex = Lexer(TupleTokens.lexmap)
data = '(1, 2, (, )'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))