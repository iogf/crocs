# crocs

Write regex using pure python class/function syntax and test it better.

The idea behind crocs is simplifying the construction and debugging of regex's. 
It is possible to implement regex's using a function/class syntax, the resulting structure 
is then compiled into a regex's string. it is as well possible to generate random inputs 
for the regex that would match the regex pattern.

It is also possible to insert a raw regex string and generate possible matches. It helps a lot
when debugging regex's. 

The project relies on [eacc](https://github.com/iogf/eacc) to build an AST for the given regex.

~~~
[tau@archlinux eacc.wiki-code]$ regxhits 
Regstr:ab*c.f
Regex: ab{0,}c.f
Input: ababababababc}f
Group dict: {}
Group 0: abc}f
Groups: ()
Match with:
 abababc3f abc3f ababababababababc%f abababababababcUf 
ababababababababababcTf abababababc(f abcmf ababababababababababcDf 
abcDf ababababc'f

~~~

A more complicated example.

~~~
[tau@archlinux ~]$ regxhits 
Regstr:a(b.?c)m.n?
Regex: a(b.{0,1}c)m.n{0,1}
Input: abdcmin
Group dict: {}
Group 0: abdcmin
Groups: ('bdc',)
Match with:
 abdcm{n   abdcmcn abdcm5n abdcmHn   abdcmSn 

~~~

With sets.

~~~
[tau@archlinux ~]$ regxhits 
Regstr:a[bc1-9]{1,4}ef
Regex: a[bc1-9]{1,4}ef
Input: a84cef
Group dict: {}
Group 0: a84cef
Groups: ()
Match with:
 ab9ef a664ef a869bef a913ef a41ef a279bef a15ef a8ef a36cef a34ef
~~~

The examples below clarifies better.

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

### Concrete Example

It solves the problem of catching mails whose domain ends with 'br'  and the hostname 
contains 'python' in the beginning too. It makes sure that the first 
letter in the mail name is in the set a-z as well.

~~~python
from crocs.regex import Seq, Include, Repeat, Join, NamedGroup, Include

# First we define how our patterns look like.
name_valid_letters = Seq('a', 'z')
name_valid_numbers = Seq('0', '9')
name_valid_signs   = '_.-'

# The include works sort of Repeat except for one char. 
# You can think of it as fetching one from the described sets.
name_valid_chars = Include(name_valid_letters, 
name_valid_numbers, name_valid_signs)

# Think of the Repeat class as meaning: fetch the
# described pattern one or more Repeat.
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

# Install

**Note:** Work with python3 only.

~~~
pip install crocs
~~~

Documentation
=============

[Wiki](https://github.com/iogf/crocs/wiki)

