# crocs

Write regex using pure python class/function syntax and test it better.

The idea behind crocs is simplifying the construction and debugging of regex's. 
It is possible to implement regex's using a function/class syntax, the resulting structure 
is then compiled into a regex's string. it is as well possible to generate random inputs 
for the regex that would match the regex pattern.

It is also possible to insert a raw regex string and generate possible matches. It helps a lot
when debugging a complex regex. 

The project relies on [eacc](https://github.com/iogf/eacc) to parse the regex string then
generating possible matches. 

### Regex Hits

The regex below is merely parsed using [eacc](https://github.com/iogf/eacc) then an AST
is generated. The AST is built using crocs's classes. Once it is built then the hits
are generated.

~~~
[tau@archlinux crocs-code]$ regxhits 
Regstr:(?P<name>[a-z][a-z0-9_\.\-]{1,})@(?P<hostname>python[a-z]{1,})\.(?P<domain>br)
Compiled Regex: (?P<name>[a-z][a-z0-9_\.\-]{1,})@(?P<hostname>python[a-z]{1,})\.(?P<domain>br)
Input: siz@pythonyz.br
Group dict: {'name': 'siz', 'hostname': 'pythonyz', 'domain': 'br'}
Group 0: siz@pythonyz.br
Groups: ('siz', 'pythonyz', 'br')
Match with:
 mg@pythonyeegr.br v0vr@pythonszvcq.br pk2rm4gh3@pythonomq.br whzevst-@pythonkzdgkh.br 
vvlx-w@pythoni.br wrngzn698mh@pythonrx.br vrisys@pythonqgpc.br u.z@pythonlkgcyut.br 
dv-@pythonf.br taxcprguso3@pythonwe.br
~~~

### Python2Regex

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

