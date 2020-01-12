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
    r_paren = Rule(TokVal('('), Struct(grammar), TokVal(')'))
    r_num = Rule(Num)
    grammar.add(r_paren, r_num)
    grammar.discard(Blank)

print('Example 1')
lex = Lexer(TupleTokens.lexmap)
data = '(1 2 3 ( 4 5 6))'
lex.feed(data)
tokens = lex.run()
yacc = Yacc(TupleGrammar.grammar)
ptree = yacc.build(tokens)
print('Consumed:', list(ptree))
