"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, Rule, Grammar, Struct, Yacc
from crocs.token import Token

class Num(Token):
    pass

class Plus(Token):
    pass

class Minus(Token):
    pass

class Div(Token):
    pass

class Mul(Token):
    pass

class RP(Token):
    pass

class LP(Token):
    pass

class Blank(Token):
    pass

class CalcTokens:
    lexmap = LexMap()
    LexNode(lexmap, r'\+', Plus)
    LexNode(lexmap, r'\-', Minus)
    LexNode(lexmap, r'\(', LP)
    LexNode(lexmap, r'\)', RP)
    LexNode(lexmap, r'\*', Mul)
    LexNode(lexmap, r'\/', Div)

    LexNode(lexmap, r'[0-9]+', Num)
    LexNode(lexmap, r' +', Blank)

class CalcGrammar:
    expression = Grammar()
    term = Grammar()
    factor = Grammar()

    Rule(expression, Struct(expression), Plus, Struct(term))
    Rule(expression, Struct(expression), Minus, Struct(term))
    Rule(expression, Struct(term))

    Rule(term, Struct(term), Mul, Struct(factor))
    Rule(term, Struct(term), Div, Struct(factor))
    Rule(term, Struct(factor))

    Rule(factor, Num)
    Rule(factor, LP, Struct(expression), RP)
    expression.discard(Blank)

class CalcParser(Yacc):
    def __init__(self):
        self.lexer = Lexer(CalcTokens.lexmap)
        super(CalcParser, self).__init__(CalcGrammar.expression)
    
    def calc(self, data):
        self.lexer.feed(data)
        tokens = self.lexer.run()
        return self.build(tokens)

data = '1 + 2 * (1 - 2)'
parser = CalcParser()
ptree = parser.calc(data)
print('Consumed:', list(ptree))



