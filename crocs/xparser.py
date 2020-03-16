from yacc.yacc import Rule, Grammar, Struct, Yacc
from yacc.lexer import Lexer, LexMap, LexNode, XSpec
from yacc.token import Plus, LP, RP, Mul, Div,\
Num, Comma, Sof, Eof

class RegexTokens(XSpec):
    lexmap = LexMap()
    t_plus   = LexNode(r'\+', Plus)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)

    t_lbracket = LexNode(r'\[', LSB)
    t_rbracket = LexNode(r'\]', RSB)

    t_lbrace = LexNode(r'\{', LP)
    t_rbrace = LexNode(r'\}', RP)
    t_comma = LexNode(r'\,', RP)

    t_mul    = LexNode(r'\*', Mul)
    t_question    = LexNode(r'\*', Question)

    t_num    = LexNode(r'[0-9]+', Num, float)
    # t_str    = LexNode(r'', Mul)

    lexmap.add(t_plus, t_minus, t_lparen, t_num, 
    t_rparen, t_mul, t_div)

    root = [expression]

class RegexGrammar(Grammar):
    regex = Struct()

    r_paren = Rule(LP, regex, RP, type=regex)
    r_done  = Rule(Sof, regex, Eof)

    expression.add(r_paren)
    
    root    = [regex]

class XParser(Yacc):
    def __init__(self):
        self.gref = {}

    def build(self, data):
        pass

