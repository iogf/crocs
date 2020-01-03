"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, Grammar, Rule, TokVal, Struct, Yacc
from crocs.token import Token

class Blank(Token):
    pass

class Num(Token):
    pass

class TestTokens:
    lexmap = LexMap()
    LexNode(lexmap, r'\(', Token),
    LexNode(lexmap, r'\)', Token)
    LexNode(lexmap, r'\]', Token)

    LexNode(lexmap, r'[0-9]+', Num)
    LexNode(lexmap, r' +', Blank)

class TestGrammar:
    grammar = Grammar()
    Rule(grammar, Struct(grammar), TokVal(']'))
    Rule(grammar, TokVal('('), Struct(grammar), TokVal(')'))
    Rule(grammar, Num)

    grammar.discard(Blank)

print('Example 1')
lex = Lexer(TestTokens.lexmap)
data = '(32 ])'
lex.feed(data)
tokens = lex.run()
yacc = Yacc(TestGrammar.grammar)
ptree = yacc.build(tokens)
print('Consumed:', list(ptree))

