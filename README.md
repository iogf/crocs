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

Crocs also implements a powerful parsing library. It uses a similar syntax to Naur Backus. The main
idea consists of implementing token patterns and specifying a type for them. When these patterns
are matched they are assigned a type and rematched against other existing patterns. That allows one
to handle some grammars in a consistent and expressive manner.

The lexer is really expressive it can handle some interesting cases in a short and simple manner.

~~~python

~~~

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

