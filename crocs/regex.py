from crocs.core import printable, RegexOperator
from random import choice, randint

class Any(RegexOperator):
    def __init__(self, *args):
        super(Any, self).__init__(*args)

    def invalid_data(self):
        lst = [ind.invalid_data() for ind in self.args]
        return choice(lst)

    def valid_data(self):
        lst = [ind.valid_data() for ind in self.args]
        return choice(lst)

    def to_regex(self):
        data = map(lambda ind: ind.to_regex(), self.args)
        data = '|'.join(data)
        return data

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
        self.data = '(%s)' % ''.join((ind.to_regex() 
        for ind in self.args))

        self.compiled = True
        Group.count   = Group.count + 1
        self.map      = '\%s' % Group.count

        self.input    = map(lambda ind: ind.valid_data(), self.args)
        self.input    = ''.join(self.input)

        return self.data

    def to_regex(self):
        if not self.compiled:
            return self.compile()
        return self.map
    
    def clear(self):
        self.data     = ''
        self.map      = ''
        Group.count   = 0
        self.compiled = False
        super(Group, self).clear()

class NamedGroup(Group):
    """
    Named groups.

    (?P<name>...)
    """

    def __init__(self, name, *args):
        super(NamedGroup, self).__init__(*args)
        self.name  = name

    def compile(self):
        self.data = r'(?P<%s>%s)' % (self.name, 
        super(Group, self).to_regex())

        self.compiled = True
        self.map      = r'(?P=%s)' % self.name

        self.input    = map(lambda ind: ind.valid_data(), self.args)
        self.input    = ''.join(self.input)

        return self.data

class NGLink(RegexOperator):
    def __init__(self, name):
        super(NGLink, self).__init__()
        self.name  = name

    def to_regex(self):
        return '(?P=%s)' % self.name

    def invalid_data(self):
        return ''

    def valid_data(self):
        return ''

class Repeat(RegexOperator):
    """
    """

    MAX = 7

    def __init__(self, regex, min=0, max=''):
        super(Repeat, self).__init__(regex)
        self.min = min
        self.max = max

        if isinstance(regex, str) and len(regex) > 1:
            self.args[0] = Group(regex)
        elif isinstance(regex, Any):
            self.args[0] = Group(regex)

    def invalid_data(self):
        lim = self.max if self.max else self.MAX
        count = randint(self.min, lim)
        
        # Get all chars that wouldnt match the underlying
        # patterns.
        data = self.args[0].invalid_data() 

        # Generate a string that wouldn't match with any 
        # of the underlying patterns.
        # Notice that Repeat(X(), 2).invalid_data() would throw
        # an exception due to X() not having invalid chars.
        return ''.join((choice(data) for ind in range(count)))

    def valid_data(self):
        lim = self.max if self.max else self.MAX
        count = randint(self.min, lim)

        data = (self.args[0].valid_data() 
            for ind in range(count))
        data = ''.join(data)

        return data 

    def to_regex(self):
        return '%s{%s,%s}' % (self.args[0].to_regex(), 
        self.min, self.max)

class ZeroOrMore(Repeat):
    def __init__(self, regex):
        super(ZeroOrMore, self).__init__(regex)

    def to_regex(self):
        return '%s*' % self.args[0].to_regex()

class OneOrMore(Repeat):
    def __init__(self, regex):
        super(OneOrMore, self).__init__(regex, 1)

    def to_regex(self):
        return '%s+' % self.args[0].to_regex()

class OneOrZero(Repeat):
    def __init__(self, regex):
        super(OneOrZero, self).__init__(regex, 0, 1)

    def to_regex(self):
        return '%s?' % self.args[0].to_regex()

class ConsumeNext(RegexOperator):
    """
    Lookbehind assertion.
    
    (?<=...) or (?<...) based on neg argument.
    """

    def __init__(self, regex0, regex1, neg=False):
        super(ConsumeNext, self).__init__(regex0, regex1)
        self.neg = neg

    def invalid_data(self):
        if self.neg:
            return self.positive()
        else:
            return self.negative()

    def valid_data(self):
        if self.neg:
            return self.negative()
        else:
            return self.positive()

    def positive(self):
        hits = '%s%s' % (self.args[0].valid_data(), 
        self.args[1].valid_data())
        return hits

    def negative(self):
        return '%s%s' % (self.args[0].invalid_data(), 
        self.args[1].valid_data())

    def to_regex(self):
        fmt = '(?<=%s)%s' if not self.neg else '(?<!%s)%s'
        return fmt % (self.args[0].to_regex(), self.args[1].to_regex())

class ConsumeBack(RegexOperator):
    """
    Lookahead assertion.

    (?=...)
    """

    def __init__(self, regex0, regex1, neg=False):
        super(ConsumeBack, self).__init__(regex0, regex1)
        self.neg = neg

    def invalid_data(self):
        if self.neg:
            return self.positive()
        else:
            return self.negative()

    def valid_data(self):
        if self.neg:
            return self.negative()
        else:
            return self.positive()

    def positive(self):
        hits = (self.args[0].valid_data(), 
        self.args[1].valid_data())
        return '%s%s' % hits

    def negative(self):
        hits = (self.args[0].valid_data(), 
        self.args[1].invalid_data())
        return '%s%s' % hits

    def to_regex(self):
        fmt = '%s(?=%s)' if not self.neg else '%s(?!%s)'
        return fmt % (self.args[0].to_regex(), self.args[1].to_regex())

class Seq(RegexOperator):
    def __init__(self, start, end):
        super(Seq, self).__init__()

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

    def to_regex(self):
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
        chars = ''.join(map(
        lambda ind: ind.valid_data(), self.args))

        data = [ind for ind in printable
        if not ind in chars]

        return choice(data)

    def valid_data(self):
        chars = ''.join(map(
        lambda ind: ind.valid_data(), self.args))

        char = choice(chars)
        return char

    def to_regex(self):
        return '[%s]' % super(Include, self).to_regex()

class Exclude(Include):
    """
    Excluding.

    [^abc]
    """
    def __init__(self, *args):
        super(Exclude, self).__init__(*args)

    def invalid_data(self):
        return super(Exclude, self).valid_data()

    def valid_data(self):
        return super(Exclude, self).invalid_data()

    def to_regex(self):
        return '[^%s]' % super(Include, self).to_regex()

class X(RegexOperator):
    """
    The dot.

    .
    """


    def __init__(self):
        super(X, self).__init__()

    def invalid_data(self):
        return ''

    def valid_data(self):
        char = choice(printable)
        return char

    def to_regex(self):
        return '.'

class Join(RegexOperator):
    """
    Setup a pattern.
    """

    def __init__(self, *args):
        super(Join, self).__init__(*args)

    def invalid_data(self):
        return ''.join(map(lambda ind: \
        ind.invalid_data(), self.args))

    def valid_data(self):
        return ''.join(map(lambda ind: \
        ind.valid_data(), self.args))

class RegexComment(RegexOperator):
    def __init__(self, comment):
        super(RegexComment, self).__init__()
        self.comment = comment

    def invalid_data(self):
        return ''

    def valid_data(self):
        return ''

    def to_regex(self):
        return r'(?#%s)' % self.comment
