# crocs

Regex-like and Naur Backus-like on python classes. An expressive parsing library.
Crocs is set of python classes that allow you to reason about regex's using a different approach.
It also implements a lexer and a Yacc-like thing whose syntax is similar to Naur Backus.

In Crocs you use classes to express regex it gets serialized to regex strings. You can also
get hits for the patteerns a given regex matches.

~~~python
from crocs.regex import Join, X

e = Join('a', X(), 'b')
e.test()
e.hits()
~~~

The above code would give you the regex's string and also possible matches.

~~~
[tau@archlinux demo]$ python wildcard.py 
Regex: a.b
Input: aob
Group dict: {}
Group 0: aob
Groups: ()
Match with:
 akb a)b aKb aSb atb a{b aTb a!b a&b a7b

~~~

A regex can be thuoght as a sequence of patterns that are joined together. Crocs offers
Regex's operators as Python classes. You reason using these classes specification to implement
your desired patterns of search.

A simple regex sequence would look like:

~~~python
from crocs.regex import Join, Include, Seq

e = Join('x', Include(Seq('0', '9')))
e.test()
e.hits()
~~~

That would give you the possible hits:

~~~
[tau@archlinux demo]$ python sequence.py 
Regex: x[0-9]
Input: x0
Group dict: {}
Group 0: x0
Groups: ()
Match with:
 x0 x2 x4 x9 x2 x5 x0 x5 x7 x3
~~~

Crocs also implements a powerful parsing library. It uses a similar syntax to Naur Backus. The main
idea consists of implementing token patterns and specifying a type for them. When these patterns
are matched they are assigned a type and rematched against other existing patterns. That allows one
to handle some grammars in a consistent and expressive manner.

The lexer is really powerful it can handle some interesting cases in a short and simple manner.

~~~python

from crocs.lexer import XSpec, Lexer, LexMap, SeqNode, LexNode, LexSeq
from crocs.token import Token, Keyword, Identifier, RP, LP, Colon

class KeywordTokens(XSpec):
    lexmap = LexMap()
    LexSeq(lexmap, SeqNode(r'if', type=Keyword),
    SeqNode(r'\s+', type=Token))

    LexNode(lexmap, r' +', type=Token)
    LexNode(lexmap, r'\(', type=LP)
    LexNode(lexmap, r'\)', type=RP)
    LexNode(lexmap, r'\:', type=Colon)

    LexNode(lexmap, r'[a-zA-Z0-9]+', type=Identifier)
    root = lexmap

lex = Lexer(KeywordTokens)
data = 'if ifnum: foobar()'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
~~~

The above example handles the task of tokenizing keywords correctly. The SeqNode class works together with
LexSeq to extract the tokens based on a given regex while LexNode works on its own to extract tokens that
do not demand a lookahead step.

The parser syntax is consistent and concrete. It allows you to link handles to token patterns and
evaluate these rules according to your necessities.

# Install

**Note:** Work with python3 only.

~~~
pip install crocs
~~~

Documentation
=============

[Wiki](https://github.com/iogf/crocs/wiki)

