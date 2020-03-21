from yacc.yacc import Rule, Grammar, Struct, Yacc
from yacc.lexer import Lexer, LexMap, LexNode, XSpec
from yacc.token import Plus, LP, RP, Mul, \
Comma, Sof, Eof, Char,  LB, RB, Question, Equal, Hash,\
LBR, RBR

class RegexTokens(XSpec):
    lexmap = LexMap()
    t_plus = LexNode(r'\+', Plus)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)

    t_lbracket = LexNode(r'\[', LB)
    t_rbracket = LexNode(r'\]', RB)

    t_lbrace = LexNode(r'\{', LBR)
    t_rbrace = LexNode(r'\}', RBR)
    t_comma  = LexNode(r'\,', Comma)
    t_question = LexNode(r'\*', Question)

    t_mul   = LexNode(r'\*', Mul)

    t_char  = LexNode(r'.', Char)
    t_hash  = LexNode(r'\#', Hash)
    t_equal = LexNode(r'\=', Equal)

    lexmap.add(t_plus, t_lparen, 
    t_rparen, t_mul, t_char, t_lbracket, t_rbracket,
    t_lbrace, t_rbrace, t_comma, t_question,
    t_char,t_hash, t_equal)

    root = [lexmap]

class RegexGrammar(Grammar):
    regex = Struct()

    r_paren = Rule(LP, regex, RP, type=regex)
    r_done  = Rule(Sof, regex, Eof)

    regex.add(r_paren, r_done)
    root    = [regex]

class XParser(Yacc):
    def __init__(self):
        self.gref = {}

    def build(self, data):
        pass

