# crocs

Write regex using pure python class/function syntax and test it better.

The idea behind crocs is simplifying the construction and debugging of regex's. It is possible to
implement regex's using a function syntax, the resulting structure is then compiled into a regex's string.
it is as well possible to generate random inputs for the regex that would match the regex pattern.

The examples below clarifies better.

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
chk = Times(x, 3)
chk.test()
~~~

The Pattern class is used to glue more than one pattern. 

### Check possible matches

~~~python
from crocs import *

p0 = Seq('a', 'z')
c0 = Include(p0)
data = Pattern('alpha', Times(c0, 1))
data.hits()
~~~

Outputs:

~~~
Match with:
alphannw alphapombn alphalidkq 
alphajoamdlvz alphaemksv alpharxu 
alphapjocfmn alphaq alphaatvtvc alphayfj

~~~

### Basic sets

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

### Using groups

~~~python
from crocs import *

e = Pattern(Group(Exclude('abc'), 'cuca'))

e.test()
~~~

Output;

~~~
Regex; ([^abc]cuca)
Input: Kcuca
Group dict: {}
Group 0: Kcuca
Groups: ('Kcuca',)
~~~

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

### Catching mails

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

### Negative lookahead

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

# Install

**Note:** Work with both python 2 or 3.

~~~
pip install crocs
~~~

Documentation
=============

[Wiki](https://github.com/iogf/crocs/wiki)






