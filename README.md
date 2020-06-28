# crocs
 
Write regex using pure python class/function syntax and test it better.

The crocs package offers a mean to implement regex using Python classes, it is basically a
pythonic way of implementing regex patterns.

There are python classes for regex operators, these classes are grouped together to form 
your desired pattern then it is serialized to a raw regex to be used with a regex engine.

The pythonic structure of a given regex pattern contains methods to test and generate possible
matches for the regex.

The project comes with a handy script regxhits that is used to read a raw regex string then
generate possible matches. It is very useful to debug debug and improve regex patterns.

The main benefits of using python to write regex it consists of the readability and 
better understanding of how your regex is working since each one of the regex pieces can be
tested separately from a python interpreter instance.

~~~python
>>> from crocs.regex import Join, ConsumeNext, X
>>> 
>>> e = ConsumeNext(Join('a', X(), 'b'), 'def')
>>> e.test()
Regex: (?<=a.b)def
Input: azbdef
Group dict: {}
Group 0: def
Groups: ()
>>> e.hits()
Match with:
 a[bdef apbdef awbdef aFbdef a:bdef a_bdef a_bdef
>>> 

~~~

The project relies on [eacc](https://github.com/iogf/eacc) to parse the regex string then
generating possible matches. 

The regexhits script helps to debug raw regex strings. It is capable of reading a given
raw regex string then generating a python structure for the regex that is used to generate the possible
matches for the regex.

~~~
[tau@archlinux ~]$ regxhits 
>>> (\ bra[a-z]il|\ bos.ia|\ germ[a-z]ny){1,4}
Regex: (\ bra[a-z]il|\ bos.ia|\ germ[a-z]ny){1,4}
Input:  germany germany germany germany
Group dict: {}
Group 0:  germany germany germany germany
Groups: (' germany',)
Match with:
  germjny germjny germjny  bos!ia  germmny germmny 
germmny germmny  germnny  bosnia  germkny  bos4ia bos4ia
~~~

The actual implementation supports most Python regex features, groups, named groups,
sets, lookahead, lookbehind etc.

### Basic Example

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
pip install -r requirements.txt 
pip install crocs
~~~

Documentation
=============

[Wiki](https://github.com/iogf/crocs/wiki)

