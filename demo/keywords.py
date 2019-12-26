"""
"""

from crocs.yacc import Lexer, LexMap, SeqNode, LexNode, LexSeq
from crocs.token import Token

class Keyword(Token):
    pass

class Identifier(Token):
    pass

class KeywordTokens:
    lexmap = LexMap()
    LexSeq(lexmap, SeqNode(r'rif', type=Keyword),
    SeqNode(r'\s+', type=Token))

    LexSeq(lexmap, SeqNode(r'for', type=Keyword),
    SeqNode(r'\s+', type=Token))

    LexSeq(lexmap, SeqNode(r'end', type=Keyword),
    SeqNode(r'\s+', type=Token))

    LexNode(lexmap, r' +', type=Token)
    LexNode(lexmap, r'[a-zA-Z0-9]+', type=Identifier)

lex = Lexer(KeywordTokens.lexmap)

print('Example 1!')
data = 'flow if foo for bar end pears'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))
