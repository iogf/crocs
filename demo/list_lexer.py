"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, SeqNode, LexRef, LexSeq
from crocs.token import Token

class ListTokens:
    lexmap = LexMap()
    LexSeq(lexmap, 
    SeqNode(r'\[', Token),
    LexRef(lexmap),
    SeqNode(r'\]', Token))

    LexNode(lexmap, r'[0-9]+', Token)
    LexNode(lexmap, r' +', Token)

print('Example 1')
lex = Lexer(ListTokens.lexmap)
data = '[ 1 2 [1 3 4] [2 4 [ 1 2]]]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2')
lex = Lexer(ListTokens.lexmap)
data = '[1 2] ]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


