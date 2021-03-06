from crocs.core import printable, RegexOperator, isword, \
notword, RegexStr, RegexMeta, BadYregex
from random import choice, randint
from itertools import groupby

class JoinX(RegexOperator):
    def __init__(self, *args):
        items = (RegexStr(ind) if isinstance(ind, str) else ind 
        for ind in args)

        args  = []        
        opers = groupby(items, lambda ind: ind.__class__)

        for indi, indj in opers:
            args.extend(indi.reduce_initargs(*indj))
        super(JoinX, self).__init__(*args)

    def invalid_data(self):
        return ''.join(map(lambda ind: ind.invalid_data(), self.args))

    def valid_data(self):
        return ''.join(map(lambda ind: ind.valid_data(), self.args))

class Pattern(JoinX):
    """
    This class is used to join sub patterns. The sub patterns
    can be instances of Group, Repeat, str, etc. 

    the only constraint it is not possible to pass instances of Any
    otherwise it would cause ambiguity in the raw regex string.
    """

    def __init__(self, *args):
        for ind in args:
            if isinstance(ind, Any):
                raise BadYregex(('Received Any instance!' 
                    'Wrap it with a group.'))
        super(Pattern, self).__init__(*args)

class Any(RegexOperator):
    """
    The regex |.

    Usage:
        any = Any('abc', 'efg')
        print(any.mkregex())

    Output:
        'abc|efg'
    """

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

class MetaB(RegexMeta):
    """
    The regex \B.

    Usage:
        pattern = Pattern(MetaB(), 'bar')
        print(pattern.mkregex())

    Output:
        \Bbar
    """

    def invalid_data(self):
        return ''

    def valid_data(self):
        data = choice(isword) 
        return  data

    def to_regex(self):
        return r'\B'

class Metab(RegexMeta):
    """
    The regex \b.

    Usage:
        pattern = Pattern(Metab(), 'bar')
        print(pattern.mkregex())

    Output:
        \bbar
    """

    def invalid_data(self):
        return choice(isword)

    def valid_data(self):
        return ''

    def to_regex(self):
        return r'\b'

class Caret(RegexOperator):
    """
    The regex ^.

    Usage:
        pattern = Pattern(Caret(), 'bar')
        print(pattern.mkregex())

    Output:
        ^bar
    """

    def invalid_data(self):
        return r''

    def valid_data(self):
        return r''

    def to_regex(self):
        return '^' 

class Dollar(RegexOperator):
    """
    The regex $.

    Usage:

        pattern = Pattern('foobar', Dollar())
        print(pattern.mkregex())

    Output:

        foobar$
    """

    def invalid_data(self):
        return r''

    def valid_data(self):
        return r''

    def to_regex(self):
        return '$' 

class NonCapture(JoinX):
    """
    The regex:
        (:abc)

    Usage:
        group = NonCapture('foo')
        pattern = Pattern(group, 'bar')
        print(pattern.mkregex())

    Output:

        (?:foo)bar

    """
    def __init__(self, *args):
        super(NonCapture, self).__init__(*args)

    def invalid_data(self):
        data = map(lambda ind: ind.invalid_data(), self.args)
        return ''.join(data)

    def valid_data(self):
        data = map(lambda ind: ind.valid_data(), self.args)
        return ''.join(data)

    def to_regex(self):
        data = ''.join((ind.to_regex() 
        for ind in self.args))

        return '(?:%s)' % data

class Word(RegexOperator):
    """
    The \w metacharacter.

    Usage:
        repeat = Repeat(Word(), 1)
        pattern = Pattern(':', repeat)
        print(pattern.mkregex())

    Output:
        :\w{1,}

    """
    def invalid_data(self):
        return choice(notword) 

    def valid_data(self):
        return choice(isword) 

    def to_regex(self):
        return r'\w'

    def mkstmts(self, argrefs):
        return "%s = %s()" % (self.instref(argrefs), 
        self.__class__.__name__)

class NotWord(RegexOperator):
    """
    The \W metacharacter.

    Usage:
        repeat = Repeat(NotWord(), 1)
        pattern = Pattern(':', repeat)
        print(pattern.mkregex())

    Output:
        :\W{1,}

    """

    def invalid_data(self):
        return choice(isword) 

    def valid_data(self):
        return choice(notword) 

    def to_regex(self):
        return r'\W'

    def mkstmts(self, argrefs):
        return "%s = %s()" % (self.instref(argrefs), 
        self.__class__.__name__)

class Group(JoinX):
    """
    A regex group like:
        (abc)

    usage:
        group = Group('abc')
        pattern = Pattern(group, X(), group)
        print(pattern.mkregex())

    Output:
        (abc).\1

    Notice that the first reference to the group it serializes
    to the regex group construct but the second one serializes to 
    the group reference.
    """

    count = 0
    grefs  = dict()

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
        self.compiled = True
        Group.count   = Group.count + 1

        self.map      = '\%s' % Group.count
        self.grefs[Group.count] = self

        self.data = '(%s)' % ''.join((ind.to_regex() 
        for ind in self.args))

        self.input    = (ind.valid_data() for ind in self.args)
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
        Group.grefs.clear()
        self.compiled = False
        super(Group, self).clear()

class GLink(RegexOperator):
    """
    Group literal reference. It is used by the regex parser
    to index groups correctly but could be used in a yregex. 
    """
    def __init__(self, index):
        super(GLink, self).__init__()
        self.index = index

    def to_regex(self):
        return r'\%s' % self.index

    def mkregex(self):
        return self.to_regex()

    def invalid_data(self):
        group = Group.grefs[self.index]
        return group.invalid_data()

    def valid_data(self):
        group = Group.grefs[self.index]
        return group.valid_data()

    def instref(self, argrefs):
        """
        The group link lhs should be the same
        for the corresponding group, when serializing yregex to code 
        
        """

        group = Group.grefs[self.index]
        
        # Save the group attribute name in the context of the
        # yregex code.
        instname = argrefs[group]
        argrefs[self] = instname
        return instname

    def mkstmts(self, argrefs=dict()):
        name = self.instref(argrefs)

        # Shouldn't declerate statement. GLink is merely
        # a wrapper to be used when parsing raw regex.
        return ''

    def hasop(self, instance):
        return False

class NGLink(GLink):
    """
    NamedGroup reference it works alike GLink class. It is meant
    to be used by the regex parser.
    """
    def to_regex(self):
        return r'(?P=%s)' % self.index

class NamedGroup(Group):
    """
    Named groups.

    Usage:

        group = NamedGroup('gname', 'abc', X(), 'efg')
        pattern  = Pattern(group, 'ijl')
        print(pattern)

    Output:
        (?P<gname>abc.efg)ijl
    
    """

    def __init__(self, gname, *args):
        super(NamedGroup, self).__init__(*args)
        self.gname  = gname

    def compile(self):
        self.grefs[self.gname] = self

        self.data = r'(?P<%s>%s)' % (self.gname, 
        super(Group, self).to_regex())

        self.compiled = True
        self.map      = r'(?P=%s)' % self.gname

        self.input    = map(lambda ind: ind.valid_data(), self.args)
        self.input    = ''.join(self.input)

        return self.data

    def mkstmts(self, argrefs):
        name = self.instref(argrefs)
        lines = super(NamedGroup, self).mkargs_stmts(argrefs)

        args = ', '.join((argrefs[ind] for ind in self.args))
        stmt = "%s = %s('%s', %s)"
        stmt = stmt % (name, self.__class__.__name__, self.gname, args)
        lines.append(stmt)

        code = '\n'.join(lines)
        return '%s\n%s' % (code, stmt)

class Repeat(RegexOperator):
    """
    The regex a{min, max)}

    Usage:
        repeat = Repeat('a', 1)
        print(repeat)

    Output:
        a{1,}

    """

    MAX = 7

    def __init__(self, regex, min=0, max='', greedy=False):
        super(Repeat, self).__init__(regex)
        self.min    = min
        self.max    = max
        self.greedy = greedy

        if isinstance(regex, str) and len(regex) > 1:
            raise BadYregex("String length > 1! Use it with a group.")
        elif isinstance(regex, Any) or isinstance(regex, Pattern):
            raise BadYregex("Can't repeat! Wrap it with a group.")

    def invalid_data(self):
        lim = self.MAX if self.max == '' else self.max

        count = randint(self.min, lim)
        data = self.args[0].invalid_data() 

        # Generate a string that wouldn't match with any 
        # of the underlying patterns.
        # Notice that Repeat(X(), 2).invalid_data() would throw
        # an exception due to X() not having invalid chars.
        return ''.join((choice(data) for ind in range(count)))

    def valid_data(self):
        lim = (self.MAX + self.min) if self.max == '' else self.max
        count = randint(self.min, lim)

        data = (self.args[0].valid_data() 
            for ind in range(0, count))
        data = ''.join(data)

        return data 

    def to_regex(self):
        sym   = '?' if self.greedy else ''
        regex = self.args[0].to_regex()

        return '%s{%s,%s}%s' % (regex, self.min, self.max, sym)

    def mkstmts(self, argrefs):
        name = self.instref(argrefs)

        code = self.args[0].mkstmts(argrefs)
        stmt = "%s = %s(%s, min=%s, max=%s, greedy=%s)"

        stmt = stmt % (name, 
        self.__class__.__name__, argrefs[self.args[0]], self.min, 
        self.max if self.max != '' else "''", self.greedy)

        return '%s\n%s' % (code, stmt)

class ZeroOrMore(Repeat):
    """
    The regex op +. It works alike Repeat.
    """

    def __init__(self, regex, min=0, max='', greedy=False):
        super(ZeroOrMore, self).__init__(regex, 0, greedy=greedy)

    def to_regex(self):
        return '%s*%s' % (self.args[0].to_regex(), 
        '?' if self.greedy else '')

class OneOrMore(Repeat):
    """
    The regex op *. It works alike Repeat.
    """

    def __init__(self, regex, min=1, max='', greedy=False):
        super(OneOrMore, self).__init__(regex, min, max, greedy=greedy)

    def to_regex(self):
        return '%s+%s' % (self.args[0].to_regex(), 
        '?' if self.greedy else '')

class OneOrZero(Repeat):
    """
    The regex op ?.
    """

    def __init__(self, regex, min=0, max=1, greedy=False):
        super(OneOrZero, self).__init__(regex, min, max, greedy=greedy)

    def to_regex(self):
        return '%s?%s' % (self.args[0].to_regex(), 
        '?' if self.greedy else '')

class ConsumeNext(RegexOperator):
    """
    Lookbehind assertion.
    
    (?<=...) or (?<...) based on neg argument.
    """

    def __init__(self, regex0, regex1, neg=False):
        if isinstance(regex1, Any):
            raise BadYregex(('Argument regex1 is Any instance!'
                'Wrap it with a group'))

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


    def mkstmts(self, argrefs):
        name = self.instref(argrefs)

        code0 = self.args[0].mkstmts(argrefs)
        code1 = self.args[1].mkstmts(argrefs)

        stmt = "%s = %s(%s, %s, neg=%s)"

        stmt = stmt % (name, self.__class__.__name__, 
        argrefs[self.args[0]], argrefs[self.args[1]], self.neg)

        return '%s\n%s\n%s' % (code0, code1, stmt)

class ConsumeBack(ConsumeNext):
    """
    The regex lookahead assertion.

        (?=foo)bar
    """

    def __init__(self, regex0, regex1, neg=False):
        if isinstance(regex1, Any):
            raise BadYregex(('Argument regex1 is Any instance!'
                'Wrap it with a group'))

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
    """
    Map to a sequence like a-z, A-Z, 0-9 etc.
    It can only be used with Include or Exclude.
    """

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

    def mkstmts(self, argrefs):
        return "%s = %s('%s', '%s')" % (self.instref(argrefs), 
        self.__class__.__name__, self.start, self.end)

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

class RegexComment(RegexOperator):
    """
    Just a regex comment like (?#foobar)
    """
    def __init__(self, comment):
        super(RegexComment, self).__init__()
        self.comment = comment

    def invalid_data(self):
        return ''

    def valid_data(self):
        return ''

    def to_regex(self):
        return r'(?#%s)' % self.comment

    def mkstmts(self, argrefs):
        return "%s = %s('%s')" % (self.instref(argrefs), 
        self.__class__.__name__, self.comment)
