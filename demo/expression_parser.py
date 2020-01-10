"""
"""

from crocs.yacc import Lexer, LexMap, LexNode, Rule, Grammar, Struct, Yacc
from crocs.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank

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
    term       = Grammar()
    factor     = Grammar()

    r_plus = Rule(expression, Plus, term, type=expression)
    r_minus = Rule(expression, Minus, term, type=expression)
    expression.add(r_plus,  r_minus, term)

    r_mul = Rule(term, Mul, factor, type=expression)
    r_div = Rule(term, Div, factor, type=expression)
    term.add(r_mul, r_div, factor)

    r_paren = Rule(LP, expression, RP, type=expression)
    r_num   = Rule(Num)
    factor.add(r_paren, r_num)

    expression.discard(Blank)

class CalcParser(Yacc):
    def __init__(self):
        self.lexer = Lexer(CalcTokens.lexmap)
        super(CalcParser, self).__init__(CalcGrammar.expression)
    
    def calc(self, data):
        self.lexer.feed(data)
        tokens = self.lexer.run()
        return self.build(tokens)

data = '1 + 2 '
parser = CalcParser()
ptree = parser.calc(data)
print('Consumed:', list(ptree))



