"""
"""

from crocs.yacc import Lexer, Yacc, LexMap, LexNode, Rule, Grammar, TokVal, Struct, XSpec
from crocs.token import Token, Blank, Eof

class NumTokens(XSpec):
    lexmap  = LexMap()
    LexNode(lexmap, r'[1-9]+', type=Token)
    LexNode(lexmap, r'\+', type=Token)

    LexNode(lexmap, r' +', type=Blank)
    root = lexmap

class NumGrammar(Grammar):
    type0   = Struct(recursive=True)
    type1   = Struct()

    r_type0 = Rule(TokVal('1'), TokVal('+'), TokVal('2'))
    type0.add(type1, r_type0)

    r_type1 = Rule(type0, TokVal('+'), TokVal('2'))
    type1.add(r_type1)

    root = type0
    discard = [Blank, Eof]

data = '1 + 2 + 2'
lexer = Lexer(NumTokens)
yacc  = Yacc(NumGrammar)
lexer.feed(data)
tokens = lexer.run()
ptree  = yacc.build(tokens)
print('Consumed:', list(ptree))

