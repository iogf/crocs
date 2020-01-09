"""
"""

from crocs.yacc import Lexer, Yacc, LexMap, LexNode, Rule, Grammar, TokVal
from crocs.token import Token, Blank

class WordTokens:
    lexmap  = LexMap()
    LexNode(lexmap, r'[a-zA-Z]+', type=Token)
    LexNode(lexmap, r' +', type=Blank)

class WordGrammar:
    grammar   = Grammar()
    r_phrase0 = Rule(TokVal('alpha'), TokVal('beta'))
    r_phrase1 = Rule(TokVal('gamma'), TokVal('zeta'))
    grammar.add(r_phrase0, r_phrase1)
    grammar.discard(Blank)

data = 'alpha beta gamma zeta'
lexer = Lexer(WordTokens.lexmap)
yacc  = Yacc(WordGrammar.grammar)
lexer.feed(data)
tokens = lexer.run()
ptree  = yacc.build(tokens)
print(list(ptree))
