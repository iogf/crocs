"""
"""

from crocs.lexer import Lexer, LexMap, LexNode, XSpec
from crocs.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank

class CalcTokens(XSpec):
    expression = LexMap()
    t_plus   = LexNode(r'\+', Plus)
    t_minus  = LexNode(r'\-', Minus)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)
    t_mul    = LexNode(r'\*', Mul)
    t_div    = LexNode(r'\/', Div)

    t_num    = LexNode(r'[0-9]+', Num, float)
    t_blank  = LexNode(r' +', Blank)

    expression.add(t_plus, t_minus, t_lparen, t_num, 
    t_blank, t_rparen, t_mul, t_div)

    root = [expression]

print('Example 1')
lex = Lexer(CalcTokens)
data = '1+1+(3*2+4)+' * 30000 + '2'
data = '1+1+(3*2+4)'

tokens = lex.feed(data)
tk = list(tokens)
print('Consumed:', tk)