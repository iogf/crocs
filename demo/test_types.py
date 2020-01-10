"""
"""

from crocs.yacc import Lexer, Yacc, LexMap, LexNode, Rule, Grammar, TokVal
from crocs.token import Token, Blank, Eof

class NumTokens:
    lexmap  = LexMap()
    LexNode(lexmap, r'[1-9]+', type=Token)
    LexNode(lexmap, r'\+', type=Token)

    LexNode(lexmap, r' +', type=Blank)

class NumGrammar:
    main   = Grammar()
    type0   = Grammar()

    r_type0 = Rule(TokVal('1'), TokVal('+'), TokVal('2'), type=type0)
    main.add(r_type0)
    main.discard(Blank, Eof)

    r_type1 = Rule(type0, TokVal('+'), TokVal('2'))
    type0.add(r_type1)

data = '1 + 2 + 2'
lexer = Lexer(NumTokens.lexmap)
yacc  = Yacc(NumGrammar.main)
lexer.feed(data)
tokens = lexer.run()
ptree  = yacc.build(tokens)
print('Consumed:', list(ptree))

