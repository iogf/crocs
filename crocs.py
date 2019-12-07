from random import choice, randint
from string import printable
import re

class RegexStr:
    def __init__(self, value):
        self.value = value

    def invalid_data(self):
        # data = filter(lambda ind: \
        # not ind in self.value, printable)

        data = [ind for ind in printable
        if not ind in self.value]

        return ''.join(choice(data) 
        for ind in range(len(self.value)))

    def valid_data(self):
        return self.value

    def __str__(self):
        return re.escape(self.value)

    def clear(self):
        pass

class RegexOperator:
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
        """
        """

        regex, data = self.seed()

        # It has to be search in order to work with ConsumeNext.
        strc  = re.search(regex, data)
        print('Regex;', regex)
        print('Input:', data)

        print('Group dict:', 
        strc.groupdict() if hasattr(
        strc, 'groupdict') else None)

        print('Group 0:', 
        strc.group(0) if hasattr(
        strc, 'group') else None)

        print('Groups:', 
        strc.groups() if hasattr(
            strc, 'groups') else None)
    
    def clear(self):
        for ind in self.args:
            ind.clear()

    def seed(self):
        self.clear()
        regex = str(self)
        input = self.valid_data()
        return regex, input

    def join(self):
        data = map(lambda ind: str(ind), self.args)
        return ''.join(data)

    def hits(self, count=10):
        data = (self.seed()[1] for ind in range(count))
        print('Match with:\n', ' '.join(data))

        # print('Fail with:\n', ' '.join((self.invalid_data() 
        # for ind in range(count))))
        
    @property
    def to_regex(self):
        return self.seed()[0]

    def __str__(self):
        pass

class Any(RegexOperator):
    def __init__(self, *args):
        super(Any, self).__init__(*args)

    def invalid_data(self):
        lst = [ind.invalid_data() for ind in self.args]
        return choice(lst)

    def valid_data(self):
        lst = [ind.valid_data() for ind in self.args]
        return choice(lst)

    def __str__(self):
        data = map(lambda ind: str(ind), self.args)
        data = '|'.join(data)
        return data

class NamedGroup(RegexOperator):
    """
    Named groups.

    (?P<name>...)
    """

    def __init__(self, name, *args):
        super(NamedGroup, self).__init__(*args)
        self.name  = name

    def invalid_data(self):
        data = map(lambda ind: ind.invalid_data(), self.args)
        data = ''.join(data)
        return data

    def valid_data(self):
        data = map(lambda ind: ind.valid_data(), self.args)
        data = ''.join(data)
        return data

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
        data = map(lambda ind: ind.invalid_data(), self.args)
        return ''.join(data)

    def valid_data(self):
        return self.input

    def compile(self):
        self.data     = '(%s)' % self.join()
        self.compiled = True
        Group.count   = Group.count + 1
        self.map      = '\%s' % Group.count

        # Warning: Not sure why it has to be here.
        self.input    = map(lambda ind: ind.valid_data(), self.args)
        self.input    = ''.join(self.input)

        return self.data

    def __str__(self):
        if not self.compiled:
            return self.compile()
        return self.map

    def clear(self):
        self.data     = ''
        self.map      = ''
        Group.count   = 0
        self.compiled = False

class Size(RegexOperator):
    """
    """

    MAX = 10

    def __init__(self, regex, min=0, max=''):
        super(Size, self).__init__(regex)

        self.regex = self.args[0]
        self.min   = min
        self.max   = max

    def invalid_data(self):
        lim = self.max if self.max else self.MAX
        count = randint(self.min, lim)
        
        # Get all chars that wouldnt match the underlying
        # patterns.
        data = self.args[0].invalid_data() 

        # Generate a string that wouldn't match with any 
        # of the underlying patterns.
        # Notice that Size(X(), 2).invalid_data() would throw
        # an exception due to X() not having invalid chars.
        return ''.join((choice(data) for ind in range(count)))

    def valid_data(self):
        lim = self.max if self.max else self.MAX
        count = randint(self.min, lim)

        data = (self.args[0].valid_data() 
            for ind in range(count))
        data = ''.join(data)

        return data 

    def __str__(self):
        return '%s{%s,%s}' % (self.regex, 
        self.min, self.max)

class Mul(Size):
    def __init__(self, regex):
        super(Mul, self).__init__(regex)

        self.regex = self.args[0]

    def __str__(self):
        return '%s*' % (self.regex)

class Plus(RegexOperator):
    def __init__(self, regex):
        super(Plus, self).__init__(regex, 1)

        self.regex = self.args[0]

    def __str__(self):
        return '%s+' % (self.regex)

class ConsumeNext(RegexOperator):
    """
    Lookbehind assertion.
    
    (?<=...) or (?<...) based on neg argument.
    """

    def __init__(self, regex0, regex1, neg=False):
        super(ConsumeNext, self).__init__(regex0, regex1)
        self.neg = neg

    def invalid_data(self):
        # *Warning*
        pass

    def valid_data(self):
        pattern0 = (self.args[0].valid_data(), 
        self.args[1].valid_data())

        if not self.neg:
            return '%s%s' % pattern0

        pattern1 = (self.args[0].invalid_data(), 
        self.args[1].valid_data())
        return '%s%s' % pattern1


    def __str__(self):
        fmt = '(?<=%s)%s' if not self.neg else '(?<!%s)%s'
        return fmt % (self.args[0], self.args[1])

class ConsumeBack(RegexOperator):
    """
    Lookahead assertion.

    (?=...)
    """

    def __init__(self, regex0, regex1, neg=False):
        super(ConsumeBack, self).__init__(regex0, regex1)
        self.neg = neg

    def invalid_data(self):
        # *Warning*

        pass

    def valid_data(self):
        pattern0 = (self.args[0].valid_data(), 
        self.args[1].valid_data())

        if not self.neg:
            return '%s%s' % pattern0

        pattern1 = (self.args[0].valid_data(), 
        self.args[1].invalid_data())

        return '%s%s' % pattern1

    def __str__(self):
        fmt = '%s(?=%s)' if not self.neg else '%s(?!%s)'
        return fmt % (self.args[0], self.args[1])

class Seq(RegexOperator):
    def __init__(self, start, end):
        self.start = start
        self.end   = end
        self.seq   = [chr(ind) for ind in range(
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


class RegexParser:
    def __init__(self, data):
        self.data = data

    def build(self):
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

