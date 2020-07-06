# crocs
 
The crocs package introduces the concept of yregex that is a mean of implementing regex patterns using pure
python classes. There are python classes for regex operators, these classes are grouped together to form 
your desired pattern. 

The main benefits of using python to write regex it consists of the readability and 
better understanding of how your regex is working since each one of the regex pieces can be
tested separately when using a python interpreter.

What if you had to debug the regex below to keep your job? :P

~~~
\*{1,3}(((a[0-9]c)\3{1,3}))((\$[a-z]\#)\2{1,3})\*{1,3}
~~~

You would need to ask help for some specialist. :P 
You will be able to better understand what is going on once your regex is a yregex.

~~~
[tau@archlinux ~]$ yregex
>>> \*{1,3}(((a[0-9]c)\3{1,3}))((\$[a-z]\#)\2{1,3})\*{1,3}
# Regex Details.

Input: **a8ca8c$z#a8ca8ca8ca8c*
Regex: \*{1,3}(((a[0-9]c)\3{1,3}))((\$[a-z]\#)\2{1,3})\*{1,3}
Group dict: {}
Group 0: **a8ca8c$z#a8ca8ca8ca8c*
Groups: ('a8ca8c', 'a8ca8c', 'a8c', '$z#a8ca8ca8ca8c', '$z#')
Match with:
 *a2ca2ca2ca2c$g#a2ca2ca2ca2ca2ca2ca2ca2ca2ca2ca2ca2c*** 
*a8ca8ca8c$j#a8ca8ca8ca8ca8ca8ca8ca8ca8c*  **a5ca5c$u#a5ca5c*** 
**a8ca8ca8ca8c$e#a8ca8ca8ca8c* *a6ca6ca6c$q#a6ca6ca6ca6ca6ca6c** 
**a1ca1ca1c$p#a1ca1ca1c** **a2ca2ca2c$x#a2ca2ca2c**

# Yregex/Code:

from crocs.regex import Repeat, Include, Seq, Group, GLink, Pattern
from crocs.core import RegexStr

repeat0 = Repeat('*', min=1, max=3, greedy=False)

seq0 = Seq('0', '9')
include0 = Include(seq0)

group2 = Group('a', include0, 'c')

repeat1 = Repeat(group2, min=1, max=3, greedy=False)
group1 = Group(group2, repeat1)
group0 = Group(group1)

seq1 = Seq('a', 'z')
include1 = Include(seq1)

group4 = Group('$', include1, '#')

repeat2 = Repeat(group1, min=1, max=3, greedy=False)
group3 = Group(group4, repeat2)

repeat3 = Repeat('*', min=1, max=3, greedy=False)
pattern0 = Pattern(repeat0, group0, group3, repeat3)
>>> 
~~~

**Note:** You could also use a python interpreter instance.

~~~
tau@archlinux ~]$ python
>>> from crocs.xparser import xmake
>>> yregex = xmake(r'a.b')
>>> yregex.test()
Input: a'b
Regex: a.b
Group dict: {}
Group 0: a'b
Groups: ()
>>> print(yregex.mkcode())
from crocs.regex import Pattern, X
from crocs.core import RegexStr

x0 = X()

pattern0 = Pattern('a', x0, 'b')
>>> 
~~~

The actual implementation supports most Python regex features, groups, named groups,
sets, lookahead, lookbehind etc.

What if you need to implement a regex to solve the problem below?

**Problem:** Match mails whose domain ends with 'br'  and the hostname 
contains 'python' at the beginning. The mail name and hostname should be made
only of letters in the set [a-z].

If you decide to use crocs's yregex approach then you could have comments around 
statements and you could test seperately each one of the sub patterns. It should improve
your reasoning and slow down development/debugging time.

~~~python
from crocs.regex import Seq, Include, Repeat, Pattern, NamedGroup, Include

# First we define how our Patterns look like.
name_letters = Include(Seq('a', 'z'))

# The regex {n,m} repeatition. The name should contains more
# than 0 chars.
name = Repeat(name_letters, 1)

# Create a named group to make it available after matching.
name = NamedGroup('name', name)

# The hostname part looks like the name except
# it starts with 'python' in the beginning, 
hostname = Repeat(name_letters, 1)
hostname = NamedGroup('hostname', 'python', hostname)

# The Pattern class joins the sub patterns it forms a single one.
mail = Pattern(name, '@', hostname, '.', 'br')
mail.test()
mail.hits()

~~~

That would output:

~~~
[tau@archlinux demo]$ python mails.py 
Input: pokxntfr@pythont.br
Regex: (?P<name>[a-z]{1,})@(?P<hostname>python[a-z]{1,})\.br
Group dict: {'name': 'pokxntfr', 'hostname': 'pythont'}
Group 0: pokxntfr@pythont.br
Groups: ('pokxntfr', 'pythont')
Match with:
 rn@pythonutfthab.br groex@pythonwy.br tgccu@pythonkb.br zzvy@pythontfb.br 
ylego@pythonlfx.br r@pythonthxjnf.br l@pythonj.br
~~~

# Install

The project relies on [eacc](https://github.com/iogf/eacc) to parse the regex string then
generating possible matches. 

**Note:** Work with python3 only.

~~~
pip install -r requirements.txt 
pip install crocs
~~~

Documentation
=============

[Wiki](https://github.com/iogf/crocs/wiki)

**Note:** There is a reasonable test coverage in [tests](tests.py) if you feel
likely having a good idea to improve accuracy, please let me know!

