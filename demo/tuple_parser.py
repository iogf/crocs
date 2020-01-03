"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, Grammar, Rule, TokVal, Struct, Yacc
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

class TupleGrammar:
    grammar = Grammar()
    Rule(grammar, TokVal('('), Struct(grammar), TokVal(')'))
    Rule(grammar, Num)
    grammar.discard(Blank)

print('Example 1')
lex = Lexer(TupleTokens.lexmap)
data = '(1 2 3 (7 8))'
lex.feed(data)
tokens = lex.run()
yacc = Yacc(TupleGrammar.grammar)
ptree = yacc.build(tokens)
print('Consumed:', list(ptree))
