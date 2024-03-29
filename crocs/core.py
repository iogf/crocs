from string import ascii_letters, punctuation, digits
from itertools import groupby
from random import choice
import re

printable  = ascii_letters + punctuation + digits
isword  = ascii_letters + digits + '_'

notword = ''.join((ind 
for ind in punctuation if ind != '_'))

class CrocsError(Exception):
    pass

class BadYregex(CrocsError):
    pass

class BasicRegex:
    def __init__(self, *args):
        self.args  = list(args)

    @classmethod
    def reduce_initargs(cls, *args):
        return args

    def clear(self):
        pass

    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def to_regex(self):
        """ 
        Shouldn't be used. Use mkregex 
        """

        lm     = lambda ind: ind.to_regex()
        regstr =  ''.join(map(lm, self.args))
        # self.clear()
        return regstr

    def mkregex(self):
        """
        Generate a raw regex.
        
        """
        regstr = self.to_regex()
        self.clear()
        return regstr

    def hasop(self, instance):
        if instance in self.args:
            return True

        for ind in self.args:
            if ind.hasop(instance):
                return True
        return False

    def iswrapper(self):
        return False

    def instref(self, argrefs):
        count = argrefs.setdefault(self.__class__, 0)
        name  = '%s%s' % (self.__class__.__name__.lower(), count)
        argrefs[self] = name
        argrefs[self.__class__] += 1
        return name

    def mkargs_stmts(self, argrefs=dict()):
        lines = []
        for ind in self.args:
            lines.append(ind.mkstmts(argrefs))
        return lines

    def mkstmts(self, argrefs=dict()):
        name = self.instref(argrefs)
        lines = self.mkargs_stmts(argrefs)

        args = ', '.join((argrefs[ind] for ind in self.args))
        stmt = '%s = %s(%s)' % (name, self.__class__.__name__, args)
        lines.append(stmt)

        code = '\n'.join((ind 
        for ind in lines if ind != ''))

        return code

    def group_imports(self, argrefs):
        groups = dict()
        classes = (ind for ind in argrefs.keys()
        if ind.__class__ is not type)

        for ind in classes:
            if ind.iswrapper() is False:
                groups.setdefault(ind.__class__.__module__, 
                    set()).add(ind.__class__.__name__)
        return groups

    def mkcode(self, argrefs=dict()):
        # Necessary to populate Group.grefs.
        regstr = self.to_regex()

        code0 = self.mkstmts(argrefs)
        modules = self.group_imports(argrefs)

        stmt = 'from %s import %s'
        code1 = '\n'.join((stmt % (indi, ', '.join(indj)) 
        for indi, indj in modules.items()))

        code2 = '%s\n%s' % (code1, code0)
        self.clear()

        return code2

    def mkclone(self):
        """
        Return a clone based on its own serialization
        to raw python code. it is mostly used for tests.
        """
        regstr = self.to_regex()

        env = dict()
        code = self.mkcode(env)
        instname = env[self]
        exec(code, env)
        self.clear()

        return env[instname]
    
class RegexStr(BasicRegex):
    def __init__(self, value):
        super(RegexStr, self).__init__(value)

    @classmethod
    def reduce_initargs(cls, *args):
        items = []
        for ind in args:
            items.append(ind.args[0])
        data = ''.join(items)
        xstr = RegexStr(data)
        return (xstr, )

    def invalid_data(self):
        data = [ind for ind in printable
        if not ind in self.args[0]]

        return ''.join(choice(data) 
        for ind in range(len(self.args[0])))

    def valid_data(self):
        return self.args[0]

    def __len__(self):
        return len(self.args[0])

    def to_regex(self):
        """
        This method uses re.escape to escape possible regex operators.

        The regex operators are escaped even inside character sets thus
        the resulting yregex from xmake may differ from the regex passed.
        """
        return re.escape(self.args[0])

    def mkregex(self):
        regstr = self.to_regex()
        return regstr

    def hasop(self, instance):
        return False

    def iswrapper(self):
        return True

    def instref(self, argrefs):
        count = argrefs.setdefault(self.__class__, 0)
        argrefs[self] = "'%s'" % self.args[0]
        argrefs[self.__class__] += 1
        return "'%s'" % self.args[0]

    def mkstmts(self, argrefs=dict()):
        self.instref(argrefs)
        return ''

    __str__ = to_regex

class BlankX(BasicRegex):
    def invalid_data(self):
        return r'x'

    def valid_data(self):
        return r''

    def to_regex(self):
        return r''

    def mkregex(self):
        return r''

class RegexOperator(BasicRegex):
    def __init__(self, *args):
        items = (RegexStr(ind) if isinstance(ind, str) else ind 
        for ind in args)

        super(RegexOperator, self).__init__(*items)

    def test(self):
        """
        Serialize the yregex that correponds to the nested 
        classes to a raw regex string. 

        Note: In case crocs can't find a valid input
        it raises an exception.
        """

        regstr = self.to_regex()

        # Make sure the regex is valid.
        regexc = re.compile(regstr)
        data   = self.valid_data()

        # It has to be search in order to work with ConsumeNext.
        regex = regexc.search(data)
        assert regex is not None, 'Failed to generate valid matches!'

        print('Input:', repr(data))
        print('Regex:', regstr)

        print('Group dict:', 
        regex.groupdict() if hasattr(
        regex, 'groupdict') else None)

        print('Group 0:', 
        regex.group(0) if hasattr(
        regex, 'group') else None)

        print('Groups:', 
        regex.groups() if hasattr(
            regex, 'groups') else None)
        self.clear()

    def clear(self):
        for ind in self.args:
            ind.clear()

    def seed(self):
        regex = self.to_regex()
        data  = self.valid_data()
        regc  = re.search(regex, data)
        self.clear()

        if regc:
            return data
        return ''

    def hits(self, count=7):
        """
        Generate possible matches/hits..
        """
        data = (self.seed() for ind in range(count))
        print('Match with:\n', ' '.join(data))

    def __str__(self):
        return self.mkregex()

class RegexMeta(RegexOperator):
    def mkstmts(self, argrefs):
        return "%s = %s()" % (self.instref(argrefs), 
        self.__class__.__name__)

