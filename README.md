# crocs

Write regex using pure python class/function syntax and test it better.

The idea behind crocs is simplifying the construction and debugging of regex's. It is possible to
implement regex's using a function syntax, the resulting structure is then compiled into a regex's string.
it is as well possible to generate random inputs for the regex that would match the regex pattern.

The example below clarifies the scenary:

~~~python
from crocs import *

e = Pattern(Group(Exclude('abc'), 'cuca'), Times(
NamedGroup('alpha', Include('mnc'), 'done'), 4))

e.test()

~~~

Would output:

~~~
[tau@sigma demo]$ python2 groups.py 
Regex; ([^abc]cuca)(?P<alpha>[mnc]done){4,}
Input: lcucandonendonendonendonendonendonendonendonendonendone
Group dict: {'alpha': 'ndone'}
Group 0: lcucandonendonendonendonendonendonendonendonendonendone
Groups: ('lcuca', 'ndone')
~~~

The input is generated randomly. So it is possible to get an intuition of how the regex will
behave with real input.

Another example:

~~~python
from crocs import *

e = Pattern(Group(Exclude('abc'), 'cuca'), Times(
NamedGroup('alpha', Include('mnc'), 'done'), 4))

e.test()
~~~

Output;

~~~
[tau@sigma demo]$ python2 basic_sets.py 
Regex; .[^abc]{3,}[xv]{4,}
Input: GVVVxxxxxxx
Group dict: {}
Group 0: GVVVxxxxxxx
Groups: ()
~~~

A simpler example that shows how to match one or more chars.

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

The module is documented and it shouldn't be hard to figure out
which classes belong to which regex operators.

**Note:** crocs is in its early development state it is not supporting all regex's features.
Check the demo folder for better info on what it can be done.

# Install

~~~
pip2 install crocs
~~~

