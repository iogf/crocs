from __future__ import print_function
from random import choice, randint
from string import printable
import re

try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3

class RegexStr(object):
    def __init__(self, value):
        self.value = value

    def invalid_data(self):
        # data = filter(lambda ind: \
        # not ind in self.value, printable)

        data = [ind for ind in printable
        if not ind in self.value]

        return ''.join(choice(data) 
        for ind in xrange(len(self.value)))

    def valid_data(self):
        return self.value

    def __str__(self):
        return re.escape(self.value)

    def clear(self):
        pass

class RegexOperator(object):
    # It may be interesting to have a base class Pattern
    # that implements common methods with Group and Include, Exclude.
    # Because these accept multiple arguments.

    def __init__(self, *args):
        self.args = [RegexStr(ind) 
        if isinstance(ind, str) else ind for ind in args]

    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def test(self):
        regex, data = self.seed()

        # It has to be search in order to work with ConsumeNext.
        strc  = re.search(regex, data)
        print('Regex;', regex)
        print('Input:', data)
        print('Group dict:', strc.groupdict())
        print('Group 0:', strc.group(0))
        print('Groups:', strc.groups())
    
    def clear(self):
        for ind in self.args:
            ind.clear()

    def seed(self):
        self.clear()
        regex = str(self)
        input = self.valid_data()

        return regex, input

    def join(self):
        return ''.join(map(lambda ind: str(ind), self.args))

    def hits(self, count=10):
        print('Match with:\n', ' '.join((self.seed()[1]
        for ind in xrange(count))))

        # print('Fail with:\n', ' '.join((self.invalid_data() 
        # for ind in xrange(count))))
        
    @property
    def to_regex(self):
        return self.seed()[0]

    def __str__(self):
        pass

class Any(RegexOperator):
    def __init__(self, *args):
        super(Any, self).__init__(*args)

    def invalid_data(self):
        return choice([ind.invalid_data() 
        for ind in self.args])

    def valid_data(self):
        return choice([ind.valid_data() 
        for ind in self.args])

    def __str__(self):
        return '|'.join(map(lambda ind: \
        str(ind), self.args))

class NamedGroup(RegexOperator):
    """
    Named groups.

    (?P<name>...)
    """

    def __init__(self, name, *args):
        super(NamedGroup, self).__init__(*args)
        self.name  = name

    def invalid_data(self):
        return ''.join(map(lambda ind: \
        ind.invalid_data(), self.args))

    def valid_data(self):
        return ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

    def __str__(self):
        return '(?P<%s>%s)' % (self.name, self.join())

class Group(RegexOperator):
    """
    A normal group.

    (abc).
    """

    count = 0

    def __init__(self, *args):
        self.compiled = False
        self.data     = ''
        self.map      = ''

        self.input    = ''
        super(Group, self).__init__(*args)

    def invalid_data(self):
        return ''.join(map(lambda ind: \
        ind.invalid_data(), self.args))

    def valid_data(self):
        return self.input

    def compile(self):
        self.data     = '(%s)' % self.join()
        self.compiled = True
        Group.count   = Group.count + 1
        self.map      = '\%s' % Group.count
        self.input    = ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

        return self.data

    def __str__(self):
        if not self.compiled:
            return self.compile()
        return self.map

    def clear(self):
        self.data = ''
        self.map  = ''
        Group.count = 0
        self.compiled = False

class Times(RegexOperator):
    """
    Match n, m times.

    a{1, 3}

    Note: The * and + are emulated by
    Times(regex, 0) or Times(regex, 1)

    """

    MAX = 10

    def __init__(self, regex, min=0, max=''):
        # The self.args will contain just one regex.
        super(Times, self).__init__(regex)

        self.regex = self.args[0]
        self.min   = min
        self.max   = max

    def invalid_data(self):
        count = randint(self.min, self.max 
        if self.max else self.MAX)
        
        # Get all chars that wouldnt match the underlying
        # patterns.
        data = self.args[0].invalid_data() 

        # Generate a string that wouldn't match with any 
        # of the underlying patterns.
        # Notice that Times(X(), 2).invalid_data() would throw
        # an exception due to X() not having invalid chars.
        return ''.join((choice(data) for ind in xrange(count)))

    def valid_data(self):
        count = randint(self.min, self.max 
        if self.max else self.MAX)

        data = ''.join((self.args[0].valid_data() 
        for ind in xrange(count)))

        return data 

    def __str__(self):
        return '%s{%s,%s}' % (self.regex, 
        self.min, self.max)

class ConsumeNext(RegexOperator):
    """
    Lookbehind assertion.
    
    (?<=...) or (?<...) based on neg argument.
    """

    def __init__(self, regex0, regex1, neg=False):
        super(ConsumeNext, self).__init__(regex0, regex1)
        self.neg = neg

    def invalid_data(self):
        pass

    def valid_data(self):
        return '%s%s' % ((self.args[0].valid_data(), 
        self.args[1].valid_data()) if not self.neg \
        else (self.args[0].invalid_data(), 
        self.args[1].valid_data()))

    def __str__(self):
        return ('(?<=%s)%s' if not self.neg else \
        '(?<!%s)%s') % (self.args[0], self.args[1])

class ConsumeBack(RegexOperator):
    """
    Lookahead assertion.

    (?=...)
    """

    def __init__(self, regex0, regex1, neg=False):
        super(ConsumeBack, self).__init__(regex0, regex1)
        self.neg = neg

    def invalid_data(self):
        pass

    def valid_data(self):
        return '%s%s' % ((self.args[0].valid_data(), 
        self.args[1].valid_data()) if not self.neg else \
        (self.args[0].valid_data(), self.args[1].invalid_data()))

    def __str__(self):
        return ('%s(?=%s)' if not self.neg else\
        '%s(?!%s)') % (self.args[0], self.args[1])

class Seq(RegexOperator):
    def __init__(self, start, end):
        self.start = start
        self.end   = end
        self.seq   = [chr(ind) for ind in xrange(
        ord(self.start), ord(self.end) + 1)]

    def invalid_data(self):
        data = [ind for ind in printable
        if not ind in self.seq]
        return ''.join(data)

    def valid_data(self):
        return ''.join(self.seq)

    def __str__(self):
        return '%s-%s' % (self.start, self.end)

    def clear(self):
        pass

class Include(RegexOperator):
    """
    Sets.

    [abc]
    """

    def __init__(self, *args):
        super(Include, self).__init__(*args)

    def invalid_data(self):
        chars = ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

        # data = filter(lambda ind: \
        # not ind in chars, printable)

        data = [ind for ind in printable
        if not ind in chars]

        return choice(data)

    def valid_data(self):
        chars = ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

        char = choice(chars)
        return char

    def __str__(self):
        return '[%s]' % self.join()

class Exclude(Include):
    """
    Excluding.

    [^abc]
    """

    def invalid_data(self):
        return super(Exclude, self).valid_data()

    def valid_data(self):
        return super(Exclude, self).invalid_data()

    def __str__(self):
        return '[^%s]' % self.join()

class X(RegexOperator):
    """
    The dot.

    .
    """

    TOKEN = '.'

    def __init__(self):
        pass

    def invalid_data(self):
        return ''

    def valid_data(self):
        char = choice(printable)
        return char

    def __str__(self):
        return self.TOKEN

    def clear(self):
        pass

class Pattern(RegexOperator):
    """
    Setup a pattern.
    """

    def __init__(self, *args):
        super(Pattern, self).__init__(*args)

    def invalid_data(self):
        return ''.join(map(lambda ind: \
        ind.invalid_data(), self.args))

    def valid_data(self):
        return ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

    def __str__(self):
        return self.join()

# Shorthands.
A  = Any
NG = NamedGroup
G  = Group
T  = Times
CN = ConsumeNext
CB = ConsumeBack
S  = Seq
I  = Include
E  = Exclude
P  = Pattern

