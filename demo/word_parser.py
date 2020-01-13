"""
"""

from crocs.yacc import Lexer, Yacc, LexMap, LexNode, Rule, Grammar, TokVal, Struct
from crocs.token import Token, Blank

class WordTokens:
    lexmap  = LexMap()
    LexNode(lexmap, r'[a-zA-Z]+', type=Token)
    LexNode(lexmap, r' +', type=Blank)

class WordGrammar(Grammar):
    expression = Struct()
    r_phrase0  = Rule(TokVal('alpha'), TokVal('beta'))
    r_phrase1  = Rule(TokVal('gamma'), TokVal('zeta'))
    expression.add(r_phrase0, r_phrase1)

    root = expression
    discard = [Blank]

data = 'alpha beta gamma zeta'
lexer = Lexer(WordTokens.lexmap)
yacc  = Yacc(WordGrammar)
lexer.feed(data)
tokens = lexer.run()
ptree  = yacc.build(tokens)
print(list(ptree))
