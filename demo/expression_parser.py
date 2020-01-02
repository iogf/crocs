"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, Rule, Grammar
from crocs.token import Token

class Num(Token):
    pass

class Op(Token):
    pass

class CalcTokens:
    lexmap = LexMap()
    LexNode(l_exp, r'\+', Token)
    LexNode(l_exp, r'\-', Token)
    LexNode(l_exp, r'\(', Token)
    LexNode(l_exp, r'\)', Token)
    LexNode(l_exp, r'\*', Token)
    LexNode(l_exp, r'\/', Token)

    LexNode(l_exp, r'[0-9]+', Token)
    LexNode(l_exp, r' +', Token)

class CalcGrammar:
    grammar = Grammar()

class CalcParser(Yacc):
    def __init__(self):
        self.lexer = Lexer(CalcTokens.l_exp)
        super(CalcParser, self).__init__(CalcGrammar.g_exp)
    
    def calc(self, data):
        self.lexer.feed(data)
        tokens = self.lexer.run()
        self.build(tokens)

    def 

data = '1 + 2 (-1 + (1 - 2)*3)'
tokens = lex.run()
yacc = Yacc()
print('Consumed:', list(tokens))




