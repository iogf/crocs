"""
"""

from crocs.lexer import XSpec, Lexer, LexMap, SeqNode, LexNode, LexSeq
from crocs.token import Token, Keyword, Identifier, RP, LP, Colon, Blank

class KeywordTokens(XSpec):
    lexmap = LexMap()
    t_if = LexSeq(SeqNode(r'if', type=Keyword),
    SeqNode(r'\s+', type=Blank))

    t_blank  = LexNode(r' +', type=Blank)
    t_lparen = LexNode(r'\(', type=LP)
    t_rparen = LexNode(r'\)', type=RP)
    t_colon  = LexNode(r'\:', type=Colon)

    # Match identifier only if it is not an if.
    t_identifier = LexNode(r'[a-zA-Z0-9]+', type=Identifier)

    lexmap.add(t_if, t_blank, t_lparen, 
    t_rparen, t_colon, t_identifier)
    root = [lexmap]

lex = Lexer(KeywordTokens)
data = 'if ifnum: foobar()'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
