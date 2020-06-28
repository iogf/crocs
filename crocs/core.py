from string import ascii_letters, punctuation, digits
from random import choice
import re

printable = ascii_letters + punctuation + digits

class BasicRegex:
    def invalid_data(self):
        pass

    def valid_data(self):
        pass

    def clear(self):
        pass

    def to_regex(self):
        pass

    def mkregex(self):
        pass
    
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

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return re.escape(self.value)

    def clear(self):
        pass

    def to_regex(self):
        return re.escape(self.value)

    def mkregex(self):
        regstr = self.to_regex()
        return regstr

    __str__ = to_regex

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

        regex = self.mkregex()
        data = self.valid_data()

        # It has to be search in order to work with ConsumeNext.
        regc  = re.search(regex, data)

        # assert regc is not None
        print('Regex:', regex)
        print('Input:', data)

        print('Group dict:', 
        regc.groupdict() if hasattr(
        regc, 'groupdict') else None)

        print('Group 0:', 
        regc.group(0) if hasattr(
        regc, 'group') else None)

        print('Groups:', 
        regc.groups() if hasattr(
            regc, 'groups') else None)
    
    def clear(self):
        for ind in self.args:
            ind.clear()

    def seed(self):
        regex = self.mkregex()
        data = self.valid_data()
        return data

    def hits(self, count=7):
        data = (self.seed() for ind in range(count))
        print('Match with:\n', ' '.join(data))

    def to_regex(self):
        """ 
        Shouldn't be used. Use mkregex 
        """

        lm     = lambda ind: ind.to_regex()
        regstr =  ''.join(map(lm, self.args))
        # self.clear()
        return regstr

    def mkregex(self):
        regstr = self.to_regex()
        self.clear()
        return regstr

    def __str__(self):
        return self.mkregex()

