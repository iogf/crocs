# crocs

Regex-like and Backus-Naur-like on python classes.  Crocs is a set of python classes 
that allows you to reason about regex's using a different approach. It also implements 
a lexer and a Yacc-like thing whose syntax is similar to Backus-Naur.

In Crocs you use classes to express regex it gets serialized to regex strings. You can also
get hits for the patterns a given regex matches.

The fact of using python code to construct regex's patterns it allows better documenting, better debugging
which improves reliability and speeds up development.

### Wildcard

~~~python
from crocs.regex import Join, X

e = Join('a', X(), 'b')
e.test()
e.hits()
~~~

The above code would give you the regex's string and also possible matches.

~~~
Regex: a.b
Input: aob
Group dict: {}
Group 0: aob
Groups: ()
Match with:
 akb a)b aKb aSb atb a{b aTb a!b a&b a7b

~~~

A regex can be thought as a sequence of patterns that are joined together. Crocs offers
Regex's operators as Python classes. You reason using these classes specification to implement
your desired patterns of search.

### Sets

A simple regex sequence would look like:

~~~python
from crocs.regex import Join, Include, Seq

e = Join('x', Include(Seq('0', '9')))
e.test()
e.hits()
~~~

That would give you the possible hits:

~~~
Regex: x[0-9]
Input: x0
Group dict: {}
Group 0: x0
Groups: ()
Match with:
 x0 x2 x4 x9 x2 x5 x0 x5 x7 x3
~~~

### Groups

~~~python
from crocs.regex import Join, Group, X

e = Join('a', Group('b', X()))
e.test()
e.hits()
~~~

Would output.

~~~
[tau@archlinux demo]$ python group.py 
Regex: a(b.)
Input: abH
Group dict: {}
Group 0: abH
Groups: ('bH',)
Match with:
 abH abH abH abH abH abH abH abH abH abH
~~~

### A concrete Regex's example

It solves the problem of catching mails whose domain ends with 'br'  and the hostname 
contains 'python' in the beginning too. It makes sure that the first 
letter in the mail name is in the set a-z as well.

~~~python
from crocs.regex import Seq, Include, Repeat, Join, NamedGroup, Include

# First we define how our Joins look like.
name_valid_letters = Seq('a', 'z')
name_valid_numbers = Seq('0', '9')
name_valid_signs   = '_.-'

# The include works sort of Repeat except for one char. 
# You can think of it as fetching one from the described sets.
name_valid_chars = Include(name_valid_letters, 
name_valid_numbers, name_valid_signs)

# Think of the Repeat class as meaning: fetch the
# described Joins one or more Repeat.
name_chunk = Repeat(name_valid_chars, 1)

# The first letter in the mail name has to be a in 'a-z'.
name_fmt = Join(Include(name_valid_letters), name_chunk)

# Think of group as a way to keep reference
# to the fetched chunk.
name = NamedGroup('name', name_fmt)

# The random's hostname part looks like the name except
# it starts with 'python' in the beginning, 
# so we fetch the random chars.
hostname_chars = Include(name_valid_letters)
hostname_chunk = Repeat(hostname_chars, 1)

# We format finally the complete hostname Join.
hostname_fmt = Join('python', hostname_chunk)

# Keep reference for the group.
hostname = NamedGroup('hostname', hostname_fmt)

# Keep reference of the domain chunk.
domain  = NamedGroup('domain', 'br')

# Finally we generate the regex and check how it looks like.
match_mail = Join(name, '@', hostname, '.', domain)
match_mail.test()
match_mail.hits()

~~~

That would output:

~~~
[tau@archlinux demo]$ python xmails.py 
Regex: (?P<name>[a-z][a-z0-9_\.\-]{1,})@(?P<hostname>python[a-z]{1,})\.(?P<domain>br)
Input: jd7.gs2@pythontritd.br
Group dict: {'name': 'jd7.gs2', 'hostname': 'pythontritd', 'domain': 'br'}
Group 0: jd7.gs2@pythontritd.br
Groups: ('jd7.gs2', 'pythontritd', 'br')
Match with:
 ppm4nh5s@pythong.br xc61_c_qic@pythonvbyzldk.br qpq.63@pythonzwwl.br 
t8@pythongfmwhje.br pqf@pythonbofrqbrcfk.br k65vyirxs@pythonttahjeup.br 
i.e3ui._@pythonylsg.br m0@pythonubjdm.br ijbf_ktux@pythonhdlh.br rtza45@pythonerypbo.br
~~~

### Lexer

Crocs also implements a powerful parsing library. It uses a similar syntax to Backus-Naur on Python classes. 
The main idea consists of implementing token patterns and specifying a type for them. 

When patterns are matched they are assigned a type and rematched against other existing patterns. That allows one
to handle some parsing problems in a consistent and expressive manner.

The lexer is really powerful it can handle some interesting cases in a short and simple manner.

~~~python
from crocs.lexer import XSpec, Lexer, LexMap, SeqNode, LexNode, LexSeq
from crocs.token import Token, Keyword, Identifier, RP, LP, Colon, Blank

class KeywordTokens(XSpec):
    lexmap = LexMap()
    t_keyword = LexSeq(SeqNode(r'if', type=Keyword),
    SeqNode(r'\s+', type=Blank))

    t_blank  = LexNode(r' +', type=Blank)
    t_lparen = LexNode(r'\(', type=LP)
    t_rparen = LexNode(r'\)', type=RP)
    t_colon  = LexNode(r'\:', type=Colon)

    t_identifier = LexNode(r'[a-zA-Z0-9]+', type=Identifier)
    lexmap.add(t_keyword, t_blank, t_lparen, t_rparen, t_colon, t_identifier)
    root = lexmap

lex = Lexer(KeywordTokens)
data = 'if ifnum: foobar()'
tokens = lex.feed(data)
print('Consumed:', list(tokens))
~~~

The above example handles the task of tokenizing keywords correctly. The SeqNode class works together with
LexSeq to extract the tokens based on a given regex while LexNode works on its own to extract tokens that
do not demand a lookahead step.

The fact of grammar lexers being defined in such a way it also allows inheritance of token regex rules. 
That means one could easily redefine a given grammar lexer on its own to work with some other grammar in an
easy and straightforward manner..

### Yacc-like/Parser

The parser syntax is consistent and concrete. It allows you to link handles to token patterns and
evaluate these rules according to your necessities.

The below code specifies a lexer and a parsing approach for a simple expression calculator.

~~~python

from crocs.yacc import Rule, Grammar, Struct, Yacc
from crocs.lexer import Lexer, LexMap, LexNode, XSpec
from crocs.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank, Sof, Eof

class CalcTokens(XSpec):
    expression = LexMap()
    t_plus   = LexNode(r'\+', Plus)
    t_minus  = LexNode(r'\-', Minus)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)
    t_mul    = LexNode(r'\*', Mul)
    t_div    = LexNode(r'\/', Div)

    t_num    = LexNode(r'[0-9]+', Num, float)
    t_blank  = LexNode(r' +', Blank)

    expression.add(t_plus, t_minus, t_lparen, t_num, 
    t_blank, t_rparen, t_mul, t_div)

    root = expression

class CalcGrammar(Grammar):
    expression = Struct()

    r_paren = Rule(LP, Num, RP, type=Num)
    r_div   = Rule(Num, Div, Num, type=Num)
    r_mul   = Rule(Num, Mul, Num, type=Num)
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)

    r_plus  = Rule(Num, Plus, Num, type=Num, up=(o_mul, o_div))
    r_minus = Rule(Num, Minus, Num, type=Num, up=(o_mul, o_div))
    r_done  = Rule(Sof, Num, Eof)

    expression.add(r_paren, r_plus, r_minus, r_mul, r_div, r_done)
    
    discard = [Blank]
    root    = [expression]

def plus(expr, sign, term):
    return expr.val() + term.val()

def minus(expr, sign, term):
    return expr.val() - term.val()

def div(term, sign, factor):
    return term.val()/factor.val()

def mul(term, sign, factor):
    return term.val() * factor.val()

def paren(left, expression, right):
    return expression.val()

def done(sof, num, eof):
    print('Result:', num.val())
    return num.val()

data = '2 * 5 + 10 -(2 * 3 - 10 )+ 30/(1-3+ 4* 10 + (11/1))'

lexer  = Lexer(CalcTokens)
tokens = lexer.feed(data)
yacc   = Yacc(CalcGrammar)

yacc.add_handle(CalcGrammar.r_plus, plus)
yacc.add_handle(CalcGrammar.r_minus, minus)
yacc.add_handle(CalcGrammar.r_div, div)
yacc.add_handle(CalcGrammar.r_mul, mul)
yacc.add_handle(CalcGrammar.r_paren, paren)
yacc.add_handle(CalcGrammar.r_done, done)

ptree = yacc.build(tokens)
ptree = list(ptree)



~~~

That would give you:

~~~
[tau@archlinux demo]$ python calc.py 
Result: 24.612244897959183
~~~

The approach consists of defining the expression tokens in CalcTokens class then the way of these tokens
should be parsed. The CalcGrammar class defines pattern rules that when matched each one of the rules
are evaluated to a type that is rematched again against the grammar rules.

It is pretty much as if when a token pattern is matched then it produces a new token that has a type
and such a token is rematched again with the defined rules.

When two math operations are performed it results in a number according to the so defined context
of math expressions. Using such a fact we can then define the math calculator mechanism to process the result.

The parser has a lookahead mechanism based on rules as well.

~~~python
    r_plus  = Rule(Num, Plus, Num, type=Num, up=(o_mul, o_div))
~~~

The above rule will be matched only if the below rules aren't matched ahead.

~~~python
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)
~~~

When a rule is matched it will call a handle with its defined tokens pattern. You can evaluate
the tokens and return a value from the handle that will be stored in the resulting parse tree
for further processing.

You can subclass Yacc and build your own parse tree for the document easily or construct it pretty much
as it is done when processing the above expression calculator value.

The fact of matched rules producing parse trees which have a specific type and being rematched
against other tokens it all allows documents parsing in an interesting and powerful manner.

You can define types for some document structures that would be trigged with tokens in some specific
circumstances. It raises creativity and also gives the opportunity for optmizing parsing of specific documents.

When a given rule has a type and is matched its parse tree result is rematched with the next tokens.
Such a process would give you a resulting structure in the end, it is one that is no longer matched
against the defined rules.

~~~python
    r_done  = Rule(Sof, Num, Eof)
~~~

The above rule consumes the last structure and is mapped to the below handle.

~~~python
def done(sof, num, eof):
    print('Result:', num.val())
    return num.val()
~~~

That just prints the resulting value. When a given document is not entirely consumed by the parsing rules
then Crocs would raise an error. It is important to mention that rules aren't necessarily having a type.

There will exist situations that you may want to define a rule with a type just to handle some specific
parts of a given document.

### Backus-Naur Form

You may be wondering why it looks like Backus-Naur, the reason is shown below:

~~~python
class CalcGrammar(Grammar):
    expression = Struct()

    r_paren = Rule(LP, expression, RP, type=expression)

    r_div   = Rule(expression, Div, expression, type=expression)
    r_mul   = Rule(expression, Mul, expression, type=expression)
    o_div   = Rule(Div)
    o_mul   = Rule(Mul)

    r_plus  = Rule(expression, Plus, expression, type=expression, up=(o_mul, o_div))
    r_minus = Rule(expression, Minus, expression, type=expression, up=(o_mul, o_div))
    r_num = Rule(Num, type=expression)

    r_done  = Rule(Sof, expression, Eof)

    expression.add(r_paren, r_plus, r_minus, r_mul, r_div, r_num, r_done)

    root    = [expression]
    discard = [Blank]
~~~

When replacing the previous example CalcGrammar code for the above one and mapping r_num rule like.

~~~python
def num(num):
    return num.val()

~~~

Then you get something similar to:

~~~
expression : expression PLUS expression
            | expression MINUS expression
            | expression TIMES expression
            | expression DIVIDE expression
            | LPAREN expression RPAREN
            | NUMBER
~~~

The type parameter maps to expression string so defined above. There is a naur_calc.py file that implements the
Backus-Naur-like approach.

It is also interesting the fact that when a grammar is defined in such a way it allows inheritance, that is
in the same manner as it happens with the lexer definition. Thus it is possible to modify some grammar rules
or just extend a given grammar.

The idea behind Crocs arouse when i was working to abstract a set of existing tools to improve 

https://github.com/vyapp/vy

That is my vim-like thing in python.

Crocs is under heavy development, there are a lot of interesting things left to be implemented and also heavy
optmizations.

# Install

**Note:** Work with python3 only.

~~~
pip install crocs
~~~

Documentation
=============

The docs may be missing some parts however there are many examples in the demo folder.

[Wiki](https://github.com/iogf/crocs/wiki)

