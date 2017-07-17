# crocs

Write regex using pure python class/function syntax and test it better.

The idea behind crocs is simplifying the construction and debugging of regex's. It is possible to
implement regex's using a function syntax, the resulting structure is then compiled into a regex's string.
it is as well possible to generate random inputs for the regex that would match the regex pattern.

The examples below clarifies better.

### Groups

Crocs makes it easy for using '\numbers' with groups and testing them.

~~~python
from crocs import *

g = Group('X', Times(Include(Seq('0', '9')), 1, 2))
e = Pattern(g, Times(Include(Seq('a', 'z')), 1, 3), g)

e.test()
e.hits()
~~~

Outputs:

~~~
Regex; (X[0-9]{1,4})[a-z]{1,3}\1
Input: X6aotX6
Group dict: {}
Group 0: X6aotX6
Groups: ('X6',)
Match with:
 X7nX7 X44ndX44 X6988mX6988 X04eX04 X6fX6 X7blX7 X31gwwX31 X7dX7 X21rwgX21 X005rvsX005
~~~

### Operator OR

~~~
from crocs import *

p0 = Times(Include('a', 'z'), 1, 10)
p1 = Any('alpha', 'beta', p0)

p1.test()
p1.hits()
~~~

Could output:

~~~
Regex; alpha|beta|[az]{1,10}
Input: beta
Group dict: {}
Group 0: beta
Groups: ()
Match with:
 zzaazz azazaaaazz beta alpha beta a z beta beta alpha
~~~

### The dot/variable

~~~python
from crocs import *

e = Pattern(Times(X(), 3, 5))

e.test()

~~~

Output:

~~~
Regex; .{3,5}
Input: yivGY
Group dict: {}
Group 0: yivGY
Groups: ()
~~~

The class X replaces the '.' regex functionality.
The string 'yivGY' is one of the possible valid inputs
that permit a match for the construction.

Notice that it would be possible to write as:

~~~python
x = X()
chk = Times(x, 3, 5)
chk.test()
~~~

The Pattern class is used to glue more than one pattern. 

### Sets

~~~python
from crocs import *

e = Pattern(Exclude('abc'), Include('xv'))

e.test()
~~~

Would output:

~~~
Regex; [^abc][xv]
Input: Ax
Group dict: {}
Group 0: Ax
Groups: ()
~~~

The input is generated randomly. So it is possible to get an intuition of how the regex will
behave with real input.

### The +/* operators.


~~~python
from crocs import *

e = Pattern(Times(X(), 1), 'cde')

e.test()

~~~

Would output: 

~~~
[tau@sigma demo]$ python2 one_or_more.py 
Regex; .{1,}cde
Input: BBBcde
Group dict: {}
Group 0: BBBcde
Groups: ()
~~~

The operators '+' and '*' are replaced for the class Times.

~~~python
Times(regex, 1) # For +

Times(regex, 0) # For *

~~~

Notice that if you want to limit below using times.

~~~python
Times(regex, max=4)
~~~

### Named groups

~~~python
from crocs import *

e = Pattern(
    Times(Include(Seq('a', 'z')), 5), '-',
    NamedGroup('num', Include(Seq('0', '9'))))

e.test()
~~~

Output: 

~~~
Regex; [a-z]{5,}\-(?P<num>[0-9])
Input: ajrjjpoke-1
Group dict: {'num': '1'}
Group 0: ajrjjpoke-1
Groups: ('1',)
~~~

### More complete example (Mail filter)

It solves the problem of catching mails whose domain contains 
'br' in the beginning and the hostname contains 'python' in  the beginning too. 
It makes sure that the first letter in the mail name is in the set a-z as well.

~~~python

from crocs import *

# First we define how our patterns look like.
name_valid_letters = Seq('a', 'z')
name_valid_numbers = Seq('0', '9')
name_valid_signs   = '_.-'

# The include works sort of Times except for one char. 
# You can think of it as fetching one from the described sets.
name_valid_chars = Include(name_valid_letters, 
name_valid_numbers, name_valid_signs)

# Think of the Times class as meaning: fetch the
# described patterns one or more times.
name_chunk = Times(name_valid_chars, 1)

# The first letter in the mail name has to be a in 'a-z'.
name_fmt = Pattern(Include(name_valid_letters), name_chunk)

# Think of group as a way to keep reference
# to the fetched chunk.
name = NamedGroup('name', name_fmt)

# The random's hostname part looks like the name except
# it starts with 'python' in the beginning, 
# so we fetch the random chars.
hostname_chars = Include(name_valid_letters)
hostname_chunk = Times(hostname_chars, 1)

# We format finally the complete hostname pattern.
hostname_fmt = Pattern('python', hostname_chunk)

# Keep reference for the group.
hostname = NamedGroup('hostname', hostname_fmt)

# Define the domain format.
domain_fmt = Pattern('br', Include(name_valid_letters))

# Keep reference of the domain chunk.
domain  = NamedGroup('domain', domain_fmt)

# Finally we generate the regex and check how it looks like.
match_mail = Pattern(name, '@', hostname, '.', domain)
match_mail.test()

~~~

Would output:

~~~
Regex; (?P<name>[a-z][a-z0-9\_\.\-]{1,})\@(?P<hostname>python[a-z]{1,})\.(?P<domain>br[a-z])
Input: tbr@pythontfn.brq
Group dict: {'domain': 'brq', 'hostname': 'pythontfn', 'name': 'tbr'}
Group 0: tbr@pythontfn.brq
Groups: ('tbr', 'pythontfn', 'brq')
~~~

Despite of the code being more prolix, using the functional syntax permits to better reason on implementing
regex for certain situations. Using a bit of imagination it can be thought as sort of an imperative
paradigm where Times, Include, Exclude play the role of retrieving content.

### Lookahead/Lookbehind

~~~python
from crocs import *

e = Pattern(ConsumeBack('abc', 'def', neg=True))
e.test()

~~~

Output: 

~~~
Regex; abc(?!def)
Input: abcoP7
Group dict: {}
Group 0: abc
Groups: ()

~~~

**Note:** crocs is in its early development state it is not supporting all regex's features.
Check the demo folder for better info on what it can be done.

### Compressed syntax

It is possible to use the following shorthands too, in some situations it may be interesting
to have.

~~~python
from crocs import I, G, E, T, P, S

e = P('alpha', G(T(I(S('1', '5')), 1, 5)), 'beta')
e.test()
e.hits()

~~~

Outputs:

~~~
Regex; alpha([1-5]{1,5})beta
Input: alpha34341beta
Group dict: {}
Group 0: alpha34341beta
Groups: ('34341',)
Match with:
 alpha51243beta alpha131beta alpha5415beta alpha24251beta 
alpha514beta alpha4324beta alpha144beta alpha4214beta 
alpha45433beta alpha4232beta

~~~

# Install

**Note:** Work with both python 2 or 3.

~~~
pip install crocs
~~~

Documentation
=============

[Wiki](https://github.com/iogf/crocs/wiki)


**Note:** If crocs was useful to you and you feel likely supporting it, please, consider opening
an issue about a donnation :)






