"""
"""

from crocs.yacc import Yacc,  Rule, Grammar, Struct
from crocs.lexer import XSpec, Lexer, LexMap, LexNode, TokVal
from crocs.token import Token, Blank, Eof, Sof

class NumTokens(XSpec):
    lexmap  = LexMap()
    t_num = LexNode(r'[1-9]+', type=TokVal)
    t_plus = LexNode(r'\+', type=TokVal)

    t_blank = LexNode(r' +', type=Blank)
    lexmap.add(t_num, t_plus, t_blank)

    root = lexmap

class NumGrammar(Grammar):
    type0   = Struct()
    type1   = Struct()

    r_type0 = Rule(TokVal('1'), TokVal('+'), TokVal('2'), type=type0)
    type0.add(r_type0)

    r_type1 = Rule(type0, TokVal('+'), TokVal('2'), type=type1)
    r_end   = Rule(Sof, type1, Eof)
    type1.add(r_type1, r_end)

    root = [type0, type1]
    discard = [Blank]

data = '1 + 2 + 2'
lexer = Lexer(NumTokens)
yacc  = Yacc(NumGrammar)
tokens = lexer.feed(data)
ptree  = yacc.build(tokens)
print('Consumed:', list(ptree))

