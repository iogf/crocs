from eacc.eacc import Rule, Grammar, Struct, T
from eacc.lexer import LexMap, LexNode, XSpec
from eacc.token import TokVal, Plus, Minus, LP, RP, Mul, \
Comma, Sof, Eof, Char,  LB, RB, Question, Equal, Hash,\
LBR, RBR, Dot, Escape

class RegexTokens(XSpec):
    lexmap = LexMap()
    t_escape = LexNode(r'\\', Escape)
    t_plus = LexNode(r'\+', Plus)

    t_dot = LexNode(r'\.', Dot)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)

    t_lbracket = LexNode(r'\[', LB)
    t_rbracket = LexNode(r'\]', RB)

    t_lbrace = LexNode(r'\{', LBR)
    t_rbrace = LexNode(r'\}', RBR)
    t_comma  = LexNode(r'\,', Comma)
    t_question = LexNode(r'\?', Question)

    t_mul   = LexNode(r'\*', Mul)
    # t_minus  = LexNode(r'\-', Minus)

    t_hash  = LexNode(r'\#', Hash)
    t_equal = LexNode(r'\=', Equal)
    t_char  = LexNode(r'.', Char)

    lexmap.add(t_escape, t_plus, t_dot, t_lparen, 
    t_rparen, t_mul, t_lbracket, t_rbracket,
    t_lbrace, t_rbrace, t_comma, t_question,
    t_char,t_hash, t_equal, t_char)

    root = [lexmap]

class RegexGrammar(Grammar):
    regex = Struct()

    r_group  = Rule(LP, regex, RP, type=regex)
    r_dot    = Rule(Dot, type=regex)
    r_times0 = Rule(regex, LBR, Char, Comma, Char, RBR, type=regex)
    r_times1 = Rule(regex, LBR, Char, RBR, type=regex)
    r_times2 = Rule(regex, LBR, Char, Comma, RBR, type=regex)
    r_times3 = Rule(regex, LBR, Comma, Char, RBR, type=regex)
    r_times4 = Rule(regex, Mul, type=regex)
    r_times5 = Rule(regex, Question, type=regex)
    r_times6 = Rule(regex, Plus, type=regex)

    r_set    = Rule(LB, T(Char), RB, type=regex)
    r_char   = Rule(Char, type=regex)

    r_join   = Rule(T(regex, 2), type=regex)
    r_done   = Rule(Sof, regex, Eof)

    regex.add(r_group, r_dot, r_times0, r_times4, r_times5, r_times6, r_join, r_char, r_done)
    root = [regex]

class XSetGrammar(Grammar):
    regex = Struct()

    r_seq = Rule(regex, TokVal('-'), regex, type=regex)
    r_done   = Rule(Sof, regex, Eof)

    root = [regex]
