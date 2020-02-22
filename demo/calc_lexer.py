"""
"""

from crocs.lexer import Lexer, LexMap, LexNode, XSpec
from crocs.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank

class CalcTokens(XSpec):
    lexmap = LexMap()

    LexNode(lexmap, r'\+', Plus)
    LexNode(lexmap, r'\-', Minus)
    LexNode(lexmap, r'\(', LP)
    LexNode(lexmap, r'\)', RP)
    LexNode(lexmap, r'\*', Mul)
    LexNode(lexmap, r'\/', Div)

    LexNode(lexmap, r'[0-9]+', Num)
    LexNode(lexmap, r' +', Blank)
    root = lexmap

print('Example 1')
lex = Lexer(CalcTokens)
data = '1 + 2 (-1 + (1 - 2)*3)'
tokens = lex.feed(data)
print('Consumed:', list(tokens))







