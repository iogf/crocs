from random import choice, randint
from string import ascii_letters
import re

class RegexStr(object):
    def __init__(self, value):
        self.value = re.escape(value)

    def invalid_data(self):
        pass

    def valid_data(self):
        return self.value

    def __str__(self):
        return self.value

class RegexOperator(object):
    def __init__(self):
        pass

    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def encargs(self, args):
        return [RegexStr(ind) if isinstance(ind, str) else ind
        for ind in args]

    def encstr(self, regex):
        regex = RegexStr(regex) if isinstance(
        regex, str) else regex
        return regex

    def test(self):
        regex = str(self)
        data  = self.valid_data()

        # It has to be search in order to work with ConsumeNext.
        strc  = re.search(regex, data)
        print 'Regex;', regex
        print 'Input:', data
        print 'Group dict:', strc.groupdict()
        print 'Group 0:', strc.group(0)
        print 'Groups:', strc.groups()

    def __str__(self):
        pass

class NamedGroup(RegexOperator):
    """
    Named groups.

    (?P<name>...)
    """

    def __init__(self, name, *args):
        self.args = self.encargs(args)
        self.name  = name

    def invalid_data(self):
        pass

    def valid_data(self):
        return ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

    def __str__(self):
        return '(?P<%s>%s)' % (self.name, ''.join(map(
        lambda ind: str(ind), self.args)))

class Group(RegexOperator):
    def __init__(self, *args):
        self.args = self.encargs(args)

    def invalid_data(self):
        pass

    def valid_data(self):
        return ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

    def __str__(self):
        return '(%s)' % ''.join(map(lambda ind: \
        str(ind), self.args))

class Times(RegexOperator):
    """
    Match n, m times.

    a{1, 3}

    Note: The * and + are emulated by
    Times(regex, 0) or Times(regex, 1)

    """

    TEST_MAX = 10

    def __init__(self, regex, min=0, max=''):
        self.regex = self.encstr(regex)

        self.min   = min
        self.max   = max

    def invalid_data(self):
        pass

    def valid_data(self):
        count = randint(self.min, self.max 
        if self.max else self.TEST_MAX)

        data = self.regex.valid_data()
        return data * count

    def __str__(self):
        return '%s{%s,%s}' % (self.regex, 
        self.min, self.max)

class ConsumeNext(RegexOperator):
    """
    Lookbehind assertion.

    (?<=...)
    """

    def __init__(self, regex0, regex1):
        self.regex0 = self.encstr(regex0)
        self.regex1 = self.encstr(regex1)

    def invalid_data(self):
        pass

    def valid_data(self):
        return '%s%s' % (self.regex0.valid_data(), 
        self.regex1.valid_data())

    def __str__(self):
        return '(?<=%s)%s' % (self.regex0, self.regex1)

class ConsumeBack(RegexOperator):
    """
    Lookahead assertion.

    (?=...)
    """

    def __init__(self, regex0, regex1):
        self.regex0 = self.encstr(regex0)
        self.regex1 = self.encstr(regex1)

    def invalid_data(self):
        pass

    def valid_data(self):
        return '%s%s' % (self.regex0.valid_data(), 
        self.regex1.valid_data())

    def __str__(self):
        return '%s(?=%s)' % (self.regex0, self.regex1)

class Include(RegexOperator):
    """
    Sets.

    [abc]
    """

    def __init__(self, chars):
        self.chars = chars

    def invalid_data(self):
        pass

    def valid_data(self):
        char = choice(self.chars)
        return char

    def __str__(self):
        return '[%s]' % self.chars

class Exclude(RegexOperator):
    """
    Excluding.

    [^abc]
    """

    def __init__(self, chars):
        self.chars = chars

    def invalid_data(self):
        pass

    def valid_data(self):
        data = filter(lambda ind: \
        not ind in self.chars, ascii_letters)

        return choice(data)

    def __str__(self):
        return '[^%s]' % self.chars

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
        char = choice(ascii_letters)
        return char

    def __str__(self):
        return self.TOKEN

class Pattern(RegexOperator):
    """
    Setup a pattern.
    """

    def __init__(self, *args):
        self.args = self.encargs(args)

    def invalid_data(self):
        pass

    def valid_data(self):
        return ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

    def __str__(self):
        return ''.join(map(lambda ind: \
        str(ind), self.args))

    
