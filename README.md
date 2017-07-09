# crocs

Write regex using pure python class/function syntax and test it better.

The idea behind crocs is simplifying the construction and debugging of regex's. It is possible to
implement regex's using a function syntax, the resulting structure is then compiled into a regex's string.
it is as well possible to generate random inputs for the regex that would match the regex pattern.

The examples below clarifies better.

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

~~~
Regex; [a-z]{5,}\-(?P<num>[0-9])
Input: ajrjjpoke-1
Group dict: {'num': '1'}
Group 0: ajrjjpoke-1
Groups: ('1',)
~~~

**Note:** crocs is in its early development state it is not supporting all regex's features.
Check the demo folder for better info on what it can be done.

# Install

~~~
pip2 install crocs
~~~


