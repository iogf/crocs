"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, SeqNode, LexRef, LexSeq
from crocs.token import Token

class ListTokens:
    lexmap = LexMap()
    LexSeq(lexmap, 
    SeqNode('\[', Token),
    LexRef(lexmap),
    SeqNode('\]', Token))

    LexNode(lexmap, '[0-9]+', Token)
    LexNode(lexmap, ' +', Token)

print('Example 1')
lex = Lexer(ListTokens.lexmap)
data = '[1 2 3 [1 3 4] [1 2 ]]'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

