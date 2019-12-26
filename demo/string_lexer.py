"""
"""

from crocs.yacc import Lexer, LexMap, LexSeq, LexNode, SeqNode
from crocs.token import Token

class StringTokens:
    lexmap = LexMap()

    LexSeq(lexmap, 
    SeqNode(r'\"', Token),
    SeqNode(r'[^\"]+', Token),
    SeqNode(r'\"', Token))

    LexNode(lexmap, r' +', type=Token)

lex = Lexer(StringTokens.lexmap)

print('Example 1!')
data = '" This will"       "rock!"     "For sure!"'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2!')

# Now displays an error due to Tok0 not being a token nor a string.
data = '" foo" bar " boo "'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


