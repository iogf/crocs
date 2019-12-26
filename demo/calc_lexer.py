"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexRef, LexChain
from crocs.token import Token

class CalcTokens:
    exp_map = LexMap()
    factor_map = LexMap()

    # LexChain(exp_map, 
    # LexRef(factor_map),
    # LexNode('\+', Token),
    # LexRef(exp_map))

    LexChain(exp_map, 
    LexRef(factor_map),
    LexNode('\*', Token))

    # LexChain(exp_map, 
    # LexNode('\(', Token),
    # LexRef(exp_map),
    # LexNode('\)', Token))

    LexChain(factor_map, 
    LexNode('[0-9]+', Token))

    LexChain(factor_map, 
    LexNode('[a-z]+', Token))

    # LexChain(factor_map, 
    # LexRef(exp_map))

    LexChain(exp_map, LexNode(' +', Token))

print('Example 1')
lex = Lexer(CalcTokens.exp_map)
data = 'foo* bar* 123*'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


print('Example 1')
lex = Lexer(CalcTokens.exp_map)
data = 'foo* bar* 123'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))





