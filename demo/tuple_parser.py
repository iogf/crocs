"""
"""

from crocs.lexer import Lexer, LexMap, LexNode, XSpec
from crocs.yacc import Grammar, Rule, Times, Yacc, Struct
from crocs.token import Token, Blank, Num, TokVal

class TupleTokens(XSpec):
    expr = LexMap()
    LexNode(expr, r'\(', Token),
    LexNode(expr, r'\)', Token)

    LexNode(expr, r'[0-9]+', Num)
    LexNode(expr, r' +', Blank)
    root = expr

class TupleGrammar(Grammar):
    expr = Struct()
    r_paren = Rule(TokVal('('), Times(expr), TokVal(')'))
    expr.add(r_paren, Num)

    discard = [Blank]
    root = expr

print('Example 1')
lex = Lexer(TupleTokens)
data = '(1 2 3 ( 4 5 6))'
lex.feed(data)
tokens = lex.run()
yacc = Yacc(TupleGrammar)
ptree = yacc.build(tokens)
print('Consumed:', list(ptree))