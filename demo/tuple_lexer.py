"""
        offset = sum(map(len, tokens))
        data = data[offset:]
"""

from crocs.lex import Lexer, LexMap, SeqNode, LexRef, LexSeq, LexNode
from crocs.token import Token

class TupleTokens:
    lexmap = LexMap()
    LexSeq(lexmap, 
    SeqNode('\(', Token),
    LexRef(lexmap),
    SeqNode('\)', Token))

    LexSeq(lexmap, 
    SeqNode(',', Token), LexRef(lexmap))

    LexNode(lexmap, '[0-9]+', Token)
    LexNode(lexmap, ' +', Token)

print('Example 1')
lex = Lexer(TupleTokens.lexmap)
data = '(1, 2, 3, (1, 2, 3))'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 2')
lex = Lexer(TupleTokens.lexmap)
data = '(1, 2, 3, (1, 2, 3), ())'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 3')
lex = Lexer(TupleTokens.lexmap)
data = '(1, 2, (), 3, (1, 2, 3), ())'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 4')
lex = Lexer(TupleTokens.lexmap)
data = '(1, 2, (,1), (3, (1, 2, 3)))'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 5')
lex = Lexer(TupleTokens.lexmap)
data = '(1, 2,(1, 2), 4)'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 6')
lex = Lexer(TupleTokens.lexmap)
data = '(1, (), )'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))

print('Example 7')
lex = Lexer(TupleTokens.lexmap)
data = '(1, ), )'
lex.feed(data)
tokens = lex.run()
print('Consumed:', list(tokens))
