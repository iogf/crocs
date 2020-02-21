"""
"""

from crocs.lexer import Lexer, LexMap, LexNode, XSpec
from crocs.yacc import Grammar, Rule, Times, Yacc, Struct
from crocs.token import Token, Blank, Num, TokVal, Sof, Eof, LP, RP

class TupleTokens(XSpec):
    expr = LexMap()
    LexNode(expr, r'\(', LP),
    LexNode(expr, r'\)', RP)

    LexNode(expr, r'[0-9]+', Num)
    LexNode(expr, r' +', Blank)
    root = expr

class TupleGrammar(Grammar):
    expr    = Struct()
    r_num   = Rule(Num)
    r_paren = Rule(Times(r_num), type=expr)
    r_expr  = Rule(LP, expr, RP, type=expr)
    r_expr0 = Rule(LP, Times(Rule(expr)), RP, type=expr)

    r_done  = Rule(Sof, expr, Eof)

    expr.add(r_paren, r_expr, r_done, r_expr0)

    discard = [Blank]
    root = [expr]

print('Example 1')
lex = Lexer(TupleTokens)
data = '(1 2 3 4 (1))'
tokens = lex.feed(data)
yacc = Yacc(TupleGrammar)
ptree = yacc.build(tokens)
print('Consumed:', list(ptree))
