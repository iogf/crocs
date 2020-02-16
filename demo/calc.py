"""
"""

from crocs.yacc import Rule, Grammar, Struct, Yacc
from crocs.lexer import Lexer, LexMap, LexNode, XSpec
from crocs.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank, Sof, Eof

class CalcTokens(XSpec):
    expression = LexMap()
    LexNode(expression, r'\+', Plus)
    LexNode(expression, r'\-', Minus)
    LexNode(expression, r'\(', LP)
    LexNode(expression, r'\)', RP)
    LexNode(expression, r'\*', Mul)
    LexNode(expression, r'\/', Div)

    LexNode(expression, r'[0-9]+', Num, float)
    LexNode(expression, r' +', Blank)
    root = expression

class CalcGrammar(Grammar):
    expression = Struct()

    r_paren = Rule(LP, Num, RP, type=Num)

    r_div   = Rule(Num, Div, Num, type=Num)
    r_mul   = Rule(Num, Mul, Num, type=Num)
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)

    r_plus  = Rule(Num, Plus, Num, type=Num, up=(o_mul, o_div))
    r_minus = Rule(Num, Minus, Num, type=Num, up=(o_mul, o_div))

    r_done  = Rule(Sof, Num, Eof)

    expression.add(r_paren, r_plus, r_minus, r_mul, r_div, r_done)

    root    = [expression]
    discard = [Blank]

class CalcParser(Yacc):
    def __init__(self):
        self.lexer = Lexer(CalcTokens)
        super(CalcParser, self).__init__(CalcGrammar)

        self.add_handle(CalcGrammar.r_plus, self.plus)
        self.add_handle(CalcGrammar.r_minus, self.minus)
        self.add_handle(CalcGrammar.r_div, self.div)
        self.add_handle(CalcGrammar.r_mul, self.mul)
        self.add_handle(CalcGrammar.r_paren, self.paren)
        self.add_handle(CalcGrammar.r_done, self.done)

    def plus(self, expr, sign, term):
        # print('Sum:', expr, sign, term)
        return expr.val() + term.val()

    def minus(self, expr, sign, term):
        # print('Minus:', expr, sign, term)
        return expr.val() - term.val()

    def div(self, term, sign, factor):
        result = term.val()/factor.val()
        # print('Div:', term, sign, factor)
        return result

    def mul(self, term, sign, factor):
        result = term.val() * factor.val()
        # print('Mul:', term.val(), sign, factor.val())
        return result

    def paren(self, left, expression, right):
        return expression.val()

    def done(self, sof, num, eof):
        print('Result:', num.val())
        # raise Exception()
        return num.val()

    def calc(self, data):
        self.lexer.feed(data)
        tokens = self.lexer.run()
        ptree = self.build(tokens)
        ptree = list(ptree)
        return ptree

data = '2 * 5 + 10 -(2 * 3 - 10 )+ 30/(1-3+ 4* 10 + (11/1) * (2/30)- 10 +3 - (2 /(2 * (3/3)*5+(8/9))) * 8*(10/10) + (3-4*(10/40)))+' * 100 + '2'
data = '2 + 2 +' * 10000 + '2'
# data = '1+1'
parser = CalcParser()
ptree = parser.calc(data)
