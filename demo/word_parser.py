"""
"""

from crocs.yacc import Yacc, Rule, Grammar, Struct
from crocs.lexer import XSpec, Lexer, LexMap, LexNode
from crocs.token import Token, Blank, Word, TokVal, Sof, Eof

class WordTokens(XSpec):
    expr = LexMap()
    t_word = LexNode(r'[a-zA-Z]+', Word)
    t_blank = LexNode(r' +', type=Blank)

    expr.add(t_word, t_blank)
    root = expr

class WordGrammar(Grammar):
    expr = Struct()
    r_phrase0  = Rule(TokVal('alpha'), TokVal('beta'))
    r_phrase1  = Rule(TokVal('gamma'), TokVal('zeta'))
    r_sof      = Rule(Sof)
    r_eof      = Rule(Eof)

    expr.add(r_phrase1, r_phrase0, r_sof, r_eof)

    root = [expr]
    discard = [Blank]

data = 'alpha beta gamma zeta' 
lexer = Lexer(WordTokens)
yacc  = Yacc(WordGrammar)
tokens = lexer.feed(data)
ptree  = yacc.build(tokens)
print(list(ptree))
