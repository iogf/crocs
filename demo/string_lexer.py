"""
"""

from crocs.lex import Lexer, LexMap, LexNode, LexChain
from crocs.token import Token

class StringTokens:
    lexmap = LexMap()
    t_str = LexChain(lexmap, 
    LexNode('\"', Token),
    LexNode('[^\"]+', Token),
    LexNode('\"', Token))

    LexChain(lexmap, LexNode(' +', type=Token))

lex = Lexer(StringTokens.lexmap)

print('Example 1!')
data = '" This will"       "rock!"     "For sure!"'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2!')

# Now displays an error due to Tok0 not being a token nor a string.
data = '" foo" "bar " boo "'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))


data = '" alpha" beta "gamma " zeta "'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

