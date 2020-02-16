"""
"""

from crocs.yacc import Yacc, Rule, Grammar, Struct
from crocs.lexer import XSpec, Lexer, LexMap, LexNode
from crocs.token import Token, Blank, TokVal, Sof, Eof

class WordTokens(XSpec):
    expr = LexMap()
    LexNode(expr, r'[a-zA-Z]+', type=Token)
    LexNode(expr, r' +', type=Blank)
    root = expr

class WordGrammar(Grammar):
    expr = Struct()
    r_phrase0  = Rule(TokVal('alpha'), TokVal('beta'))
    r_phrase1  = Rule(TokVal('gamma'), TokVal('zeta'))
    r_sof      = Rule(Sof)
    r_eof      = Rule(Eof)

    expr.add(r_phrase0, r_phrase1, r_sof, r_eof)

    root = [expr]
    discard = [Blank]

data = 'alpha beta gamma zeta ' * 10000
lexer = Lexer(WordTokens)
yacc  = Yacc(WordGrammar)
lexer.feed(data)
tokens = lexer.run()
ptree  = yacc.build(tokens)
for ind in ptree:
    pass
# print(list(ptree))
