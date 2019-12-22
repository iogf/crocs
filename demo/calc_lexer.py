from crocs.lex import Lexer, LexMap, LexNode
from crocs.yacc import Yacc, SeqMap, SeqNode

class CalcSplit:
   l_exp = LexMap()
   l_num = LexNode(l_exp, r'[0-0]+', Num)
   l_sum = LexNode(l_exp, r'+', Sum)
   l_sub = LexNode(l_exp, r'-', Sub)
   l_rp  = LexNode(l_exp, r')', RP)
   l_lp  = LexNode(l_exp, r')', LP)
   l_blk = LexNode(l_exp, r' +', discard=True)
   

class CalcSpec:
   g_exp    = Grammar()
   g_sum    = SeqMap(g_exp)
   t_sum0   = TokNode(g_sum, Num)
   t_sum1   = TokNode(g_sum0, Sum)
   t_sum2   = TokNode(g_sum1, g_exp)
   
   t_sum3   = TokNode(g_sum, Num)
   t_sum4   = TokNode(t_sum3, Sum)
   t_sum5   = TokNode(t_sum4, Num)
   
   g_sub    = SeqMap(g_exp)
   t_sub0   = TokNode(g_sub, Num)
   t_sub1   = TokNode(t_sub0, Sub)
   t_sub2   = TokNode(t_sub1, g_exp)
   
   t_sub3   = TokNode(g_exp, Sub)
   t_sub4   = TokNode(t_sub3, Num)
   t_sub5   = TokNode(t_sub4, Sub)
   
   g_paren  = SeqMap(g_exp)
   t_paren0 = TokNode(g_paren, LP)
   t_paren1 = TokNode(t_paren0, g_exp)
   t_paren2 = TokNode(t_paren1, RP)
   
class ExpParser(Yacc):
    def __init__(self):
        lex = Lexer(CalcSplit.l_exp)
        super(ExpParser, self).__init__(self.lex)

        self.add_handle(self.sum)

    def sum(self, lhs, token, lhr):
        pass
