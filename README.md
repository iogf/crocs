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

Input: ***a0ca0ca0c$i#a0ca0ca0c*
Regex: \*{1,3}(((a[0-9]c)\3{1,3}))((\$[a-z]\#)\2{1,3})\*{1,3}
Input: ***a0ca0ca0c$i#a0ca0ca0c*
Group dict: {}
Group 0: ***a0ca0ca0c$i#a0ca0ca0c*
Groups: ('a0ca0ca0c', 'a0ca0ca0c', 'a0c', '$i#a0ca0ca0c', '$i#')
Match with:
 *a4ca4c$m#a4ca4ca4ca4ca4ca4c* ***a3ca3ca3ca3c$j#a3ca3ca3ca3c** 
**a4ca4c$g#a4ca4ca4ca4c* ***a0ca0c$y#a0ca0ca0ca0ca0ca0c* **a5ca5ca5ca5c$w#a5ca5ca5ca5c* 
*a5ca5ca5c$g#a5ca5ca5c*** *a8ca8c$x#a8ca8ca8ca8ca8ca8c*

# Yregex/Code:

from crocs.regex import Group, Include, GLink, Join, Repeat, Seq
from crocs.core import RegexStr
regexstr0 = RegexStr('*')
repeat0 = Repeat(regexstr0, min=1, max=3, wrap=False, greedy=False)
regexstr1 = RegexStr('a')
seq0 = Seq('0', '9')
include0 = Include(seq0)
regexstr2 = RegexStr('c')
group2 = Group(regexstr1, include0, regexstr2)

repeat1 = Repeat(group2, min=1, max=3, wrap=False, greedy=False)
group1 = Group(group2, repeat1)
group0 = Group(group1)
regexstr3 = RegexStr('$')
seq1 = Seq('a', 'z')
include1 = Include(seq1)
regexstr4 = RegexStr('#')
group4 = Group(regexstr3, include1, regexstr4)

repeat2 = Repeat(group1, min=1, max=3, wrap=False, greedy=False)
group3 = Group(group4, repeat2)
regexstr5 = RegexStr('*')
repeat3 = Repeat(regexstr5, min=1, max=3, wrap=False, greedy=False)
join0 = Join(repeat0, group0, group3, repeat3)
>>> 

~~~

**Note:** You could also use a python interpreter instance.

~~~
>>> from crocs.xparser import xmake
>>> yregex = xmake(r'a.b')
>>> yregex.test()
Input: a<b
Regex: a.b
Input: a<b
Group dict: {}
Group 0: a<b
Groups: ()
>>> print(yregex.mkcode())
from crocs.regex import Join, X
from crocs.core import RegexStr
regexstr0 = RegexStr('a')
x0 = X()
regexstr1 = RegexStr('b')
join0 = Join(regexstr0, x0, regexstr1)
~~~

The actual implementation supports most Python regex features, groups, named groups,
sets, lookahead, lookbehind etc.

What if you need to implement a regex to solve the problem below?

**Problem:** Match mails whose domain ends with 'br'  and the hostname 
contains 'python' at the beginning. Make sure that the first 
letter in the mail name is in the set [a-z] as well.

If you decide to use crocs's yregex approach then you could have comments around 
statements and you could test seperately each one of the sub patterns. It should improve
your reasoning and slow down development/debugging time.

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

