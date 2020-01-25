"""
"""

from crocs.lexer import Lexer, LexMap, LexNode, XSpec
from crocs.token import Token

class CalcTokens(XSpec):
    lexmap = LexMap()

    LexNode(lexmap, r'\+', Token)
    LexNode(lexmap, r'\-', Token)
    LexNode(lexmap, r'\(', Token)
    LexNode(lexmap, r'\)', Token)
    LexNode(lexmap, r'\*', Token)
    LexNode(lexmap, r'\/', Token)

    LexNode(lexmap, r'[0-9]+', Token)
    LexNode(lexmap, r' +', Token)
    root = lexmap

print('Example 1')
lex = Lexer(CalcTokens)
data = '1 + 2 (-1 + (1 - 2)*3)'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))







