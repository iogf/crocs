"""
"""

from crocs.lexer import XSpec, Lexer, LexMap, SeqNode, LexNode, LexSeq
from crocs.token import Token, Keyword, Identifier, RP, LP, Colon, Blank

class KeywordTokens(XSpec):
    lexmap = LexMap()
    LexSeq(lexmap, SeqNode(r'if', type=Keyword),
    SeqNode(r'\s+', type=Blank))

    LexNode(lexmap, r' +', type=Blank)
    LexNode(lexmap, r'\(', type=LP)
    LexNode(lexmap, r'\)', type=RP)
    LexNode(lexmap, r'\:', type=Colon)

    LexNode(lexmap, r'[a-zA-Z0-9]+', type=Identifier)
    root = lexmap

lex = Lexer(KeywordTokens)
data = 'if ifnum: foobar()'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
