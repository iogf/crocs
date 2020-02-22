"""
"""

from crocs.lexer import Lexer, LexMap, LexSeq, LexNode, SeqNode, XSpec
from crocs.token import DoubleQuote, TokVal, Blank

class StringTokens(XSpec):
    lexmap = LexMap()

    LexSeq(lexmap, 
    SeqNode(r'\"', DoubleQuote),
    SeqNode(r'[^\"]+', TokVal),
    SeqNode(r'\"', DoubleQuote))

    LexNode(lexmap, r' +', type=Blank)
    root = lexmap

lex = Lexer(StringTokens)
print('Example 1!')
data = '" This will"       "rock!"     "For sure!"'
tokens = lex.feed(data)
print('Consumed:', list(tokens))


