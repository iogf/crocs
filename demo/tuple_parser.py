"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, Grammar, Rule, TokVal, Times, Yacc, Struct
from crocs.token import Token

class Blank(Token):
    pass

class Num(Token):
    pass

class TupleTokens:
    lexmap = LexMap()
    LexNode(lexmap, r'\(', Token),
    LexNode(lexmap, r'\)', Token)

    LexNode(lexmap, r'[0-9]+', Num)
    LexNode(lexmap, r' +', Blank)

class TupleGrammar(Grammar):
    expression = Struct()
    r_paren = Rule(TokVal('('), Times(expression), TokVal(')'))
    expression.add(r_paren, Num)

    discard = [Blank]
    root = expression

print('Example 1')
lex = Lexer(TupleTokens.lexmap)
data = '(1 2 3 ( 4 5 6))'
lex.feed(data)
tokens = lex.run()
yacc = Yacc(TupleGrammar)
ptree = yacc.build(tokens)
print('Consumed:', list(ptree))
