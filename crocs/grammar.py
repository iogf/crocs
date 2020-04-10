from eacc.eacc import Rule, Grammar, Struct, T
from eacc.lexer import LexMap, LexNode, XSpec, SeqNode, LexSeq
from eacc.token import TokVal, Plus, Minus, LP, RP, Mul, \
Comma, Sof, Eof, Char,  LB, RB, Question, Equal, Hash,\
LBR, RBR, Dot, Escape, Lesser, Greater, Exclam, Caret, TokType, Num

class PNGroup(TokType):
    pass

class RegexTokens(XSpec):
    lexmap = LexMap()
    t_escape = LexSeq(SeqNode(r'\\', Escape, discard=True), SeqNode(r'.', Char))

    t_plus = LexNode(r'\+', Plus)

    t_dot = LexNode(r'\.', Dot)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)

    t_gref = LexSeq(SeqNode(r'\\', Escape), 
    SeqNode(r'[0-9]', Num))

    t_lbracket = LexNode(r'\[', LB)
    t_rbracket = LexNode(r'\]', RB)

    t_lbrace = LexNode(r'\{', LBR)
    t_rbrace = LexNode(r'\}', RBR)
    t_comma  = LexNode(r'\,', Comma)
    t_question = LexNode(r'\?', Question)
    t_caret = LexNode(r'\^', Caret)

    t_mul = LexNode(r'\*', Mul)
    # t_minus  = LexNode(r'\-', Minus)

    t_hash  = LexNode(r'\#', Hash)
    t_equal = LexNode(r'\=', Equal)
    t_exclam = LexNode(r'\!', Exclam)
    t_lesser = LexNode(r'\<', Lesser)
    t_greater = LexNode(r'\>', Greater)

    t_pngroup = LexSeq(SeqNode(r'\(', LP), 
    SeqNode(r'\?', Question), SeqNode(r'P', PNGroup))

    t_char = LexNode(r'.', Char)

    lexmap.add(t_gref, t_escape, t_pngroup, t_plus, t_dot, t_lparen, 
    t_rparen, t_mul, t_lbracket, t_rbracket, t_lbrace, t_rbrace, 
    t_comma, t_question, t_caret, t_hash, t_equal, t_lesser, 
    t_greater, t_exclam, t_char)

    root = [lexmap]

class RegexGrammar(Grammar):
    regex = Struct()
    # r_escape  = Rule(Escape, Char, type=Char)

    r_group  = Rule(LP, T(regex), RP, type=regex)
    r_ngroup = Rule(LP, Question, PNGroup,
    Lesser, T(regex), Greater, T(regex), RP, type=regex)

    r_dot    = Rule(Dot, type=regex)
    r_times0 = Rule(regex, LBR, Char, Comma, Char, RBR, type=regex)
    r_times1 = Rule(regex, LBR, Char, RBR, type=regex)
    r_times2 = Rule(regex, LBR, Char, Comma, RBR, type=regex)
    r_times3 = Rule(regex, LBR, Comma, Char, RBR, type=regex)
    r_times4 = Rule(regex, Mul, type=regex)
    r_times5 = Rule(regex, Question, type=regex)
    r_times6 = Rule(regex, Plus, type=regex)

    r_include = Rule(LB, T(Char), RB, type=regex)
    r_exclude = Rule(LB, Caret, T(Char), RB, type=regex)

    r_gref = Rule(Escape, Num, type=regex)

    r_cnext = Rule(LP, Question, Lesser, Equal, 
    T(regex), RP, T(regex), type=regex)

    r_ncnext = Rule(LP, Question, Lesser, Exclam, 
    T(regex), RP, T(regex), type=regex)

    r_cback = Rule(T(regex), LP, Question, Equal, 
    T(regex), RP, type=regex)

    r_ncback = Rule(T(regex), LP, Question, 
    Exclam, T(regex), RP, type=regex)

    r_char = Rule(Char, type=regex)
    r_done = Rule(Sof, T(regex), Eof)

    regex.add(r_gref,  r_ngroup, r_group, r_dot, r_cnext, r_ncnext, r_cback, 
    r_ncback, r_times0, r_times1, r_times2, r_times3, r_times4, 
    r_times5, r_times6, r_exclude, r_include, r_char, r_done)
    root = [regex]

class IncludeGrammar(Grammar):
    regex  = Struct()
    r_seq  = Rule(Char, TokVal('-'), Char, type=regex)
    r_char = Rule(Char, type=regex)
    r_done = Rule(Sof, T(regex), Eof)

    regex.add(r_seq, r_char, r_done)
    root = [regex]

class ExcludeGrammar(Grammar):
    regex  = Struct()
    r_seq  = Rule(Char, TokVal('-'), Char, type=regex)
    r_char = Rule(Char, type=regex)
    r_done = Rule(Sof, T(regex), Eof)

    regex.add(r_seq, r_char, r_done)
    root = [regex]
