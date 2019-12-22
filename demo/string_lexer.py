"""
"""

from crocs.lex import Lexer, LexMap, LexNode
from crocs.token import Token, Eof

class StringTokens:
    lexmap = LexMap()
    t0 = LexNode(lexmap, '\"', Token)
    t1 = LexNode(t0, '[^\"]+', Token)
    t2 = LexNode(t1, '\"', Token)
    t3 = LexNode(lexmap, ' +')
    t4 = LexNode(lexmap, '', Eof)


lex = Lexer(StringTokens.lexmap)

# print('Example 1!')
# data = '" Chunk0"'
# lex.feed(data)
# tokens = lex.run()
# print(list(tokens))

print('Example 2!')
# Now displays an error due to Tok0 not being a token nor a string.
data = '" Chunk0" "ss "'
lex.feed(data)
tokens = lex.run()
print(list(tokens))
print(lex.lexmap.expect)
