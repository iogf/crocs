from random import choice, randint
from string import ascii_letters
import re

class RegexOperator(object):
    def __init__(self):
        pass

    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def __str__(self):
        pass

class NamedGroup(RegexOperator):
    def __init__(self, name, regex):
        self.regex = regex
        self.name  = name

    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def __str__(self):
        return '(?P<%s>%s)' % (self.name, self.regex)

class Group(RegexOperator):
    def __init__(self, regex):
        self.regex = regex

    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def __str__(self):
        return '(%s)' % self.regex

class Times(RegexOperator):
    TEST_MAX = 10

    def __init__(self, regex, min=0, max=''):
        self.regex = regex
        self.min   = min
        self.max   = max

    def invalid_data(self):
        pass

    def valid_data(self):
        count = randint(self.min, self.max if self.max else self.TEST_MAX)
        data = self.regex.valid_data()
        return data * count

    def __str__(self):
        return '%s{%s,%s}' % (self.regex, 
        self.min, self.max)

class ConsumeNext(RegexOperator):
    def __init__(self, regex0, regex1):
        self.regex0 = regex0
        self.regex1 = regex1

    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def __str__(self):
        return '(?<=%s)%s' % (self.regex0, self.regex1)

class ConsumeBack(RegexOperator):
    def __init__(self, regex0, regex1):
        self.regex0 = regex0
        self.regex1 = regex1

    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def __str__(self):
        return '(?=%s)%s' % (self.regex0, self.regex1)

class Include(RegexOperator):
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
    def __init__(self, *args):
        self.args = args

    def invalid_data(self):
        pass

    def valid_data(self):
        return ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

    def __str__(self):
        return ''.join(map(lambda ind: \
        str(ind), self.args))

    




