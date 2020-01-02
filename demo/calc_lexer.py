"""
"""

from crocs.yacc import Lexer, LexMap, LexNode
from crocs.token import Token

class CalcTokens:
    lexmap = LexMap()

    LexNode(lexmap, r'\+', Token)
    LexNode(lexmap, r'\-', Token)
    LexNode(lexmap, r'\(', Token)
    LexNode(lexmap, r'\)', Token)
    LexNode(lexmap, r'\*', Token)
    LexNode(lexmap, r'\/', Token)

    LexNode(lexmap, r'[0-9]+', Token)
    LexNode(lexmap, r' +', Token)

print('Example 1')
lex = Lexer(CalcTokens.lexmap)
data = '1 + 2 (-1 + (1 - 2)*3)'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))







