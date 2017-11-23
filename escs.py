##############################################################################
from crocs import *
p = Pattern(X(), X())
p.regex()
print p
print p.args
alpha = [1, 2, 3]
s = [1 if ind in alpha else 2
for ind in [5, 3, 3]]
s
##############################################################################
from crocs import *
x = X()
chk = Times(x, 3)
chk.test()

([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})

# First we define how our patterns look like.
name_valid_letters = Seq('a', 'z')
name_valid_numbers = Seq('0', '9')
name_valid_signs    = '_.-'
name_valid_chars = Include(name_valid_letters, 
name_valid_numbers, name_valid_signs)

# Think of the Times class as meaning: fetch the
# described pattern one or more times.
name_chunk = Times(name_valid_chars, 1)

# Think of group as a way to keep reference
# to the fetched chunk.
mail = NamedGroup('name', name_chunk)

# The random's hostname part looks like the name except
# it starts with 'python' in the beginning, 
# so we fetch the random chars.
hostname_chunk = Times(name_valid_chars, 1)

# We format finally the complete hostname pattern.
hostname_fmt = Pattern('python', hostname_chunk)

# Keep reference for the group.
hostname = NamedGroup('hostname', hostname_fmt)

# Define the pattern for the domain.
domain_chars = Pattern(name_valid_letters, '.')

# Fetch the pattern that we defined earlier.
domain_chunk = Times(domain_chars, 2, 6)

# Keep reference of the domain chunk.
domain  = NamedGroup('domain', domain_chunk)

# Finally we generate the regex and check how it looks like.
match_mail = Pattern(mail, '@', hostname, domain)
match_mail.test()
##############################################################################
# abc adc adc ado aio ano amo

from crocs import *

x = X()

b = Pattern(x, 'd', x)
b.test()

##############################################################################

from crocs import Seq, Pattern

# Define the scope of the data thats a-z.
p0 = Seq('a', 'z')

# Fetch the chunk from the sequence p1.
c0 = Include(p0)

# Fetch the second chunk from all printable chars.
c1 = X()

# Build the set.
set_b = Pattern(c0, c1)
set_b.test()
##############################################################################

from crocs import Seq, Pattern

# Define the scope of the data thats a-z.
p0 = Seq('0', '9')

# Fetch anything that is not in the sequence p0.
c0 = Exclude(p0)

# Fetch the second chunk from all printable chars.
c1 = X()

# Build the set.
set_b = Pattern(c0, c1)
set_b.test()
##############################################################################

# Fetch a chunk from either a-c or '_*:/'.
c0 = Include(Seq('a', 'c'), '_*;/')

# Fetch a chunk that is not in the following rage a-z or '_*;/')
c1 = Exclude(Seq('a', 'z'), '_*;/')

# Build the set x.
set_x = Pattern(c0, c1)
set_x.test()
##############################################################################
# abcd-1
# kjldkf-3

from crocs import Seq, Times, Include

# Define our sequences with the type of chars we need.
p0 = Seq('a', 'z')
p1 = Seq('A', 'Z')

# Fetch one char of the seuences.
c0 = Include(p0, p1)

# Consume one or more chars from the same sequences
# that c0 was consuming just a char.

data0 = Times(c0, 1)

# The second part , the one after the '-'.
p2 = Seq('0', '9')
c1 = Include(p2)

# Fetch the chunks.
data1 = Times(c1, 1)

# Finally we finally build the set.
set_b = Pattern(data0, '-', data1)
set_b.test()
##############################################################################
import crocs
##############################################################################
from re import *
e = search('((a.c){1,})x',' aucaocaecx')
e
e.group(0)
e.groups()
##############################################################################
# will match.
e = search('alpha(?!(a.c){1,3})',' alphacool')

# will not.
e = search('alpha(?!(a.c){1,3})',' alphaauc')
e

##############################################################################

# abc-132
# dje-39283
# ooi-1323
# lMl-sj3
# Ouilkjs-93j
# lassll-44
##############################################################################

from crocs import *

# We define our char types, we know it is formed by
# by either ascii lower cases or upper cases.
p0 = Seq('a', 'z')
p1 = Seq('A', 'Z')

# Fetch a random char from the above seqs.
c0 = Include(p0, p1)

# Fetch one or more chars from c0.
data0 = Times(c0, 1)

# Define our pattern that is going to be used as
# a condition to extract from the strings the desired chunks.
p2 = Seq('0', '9')

# Get a random char from p2.
c1 = Include(p2)

# Get one or more chars from c1.
data1 = Times(c1, 1)

# Define the general format of the second part thats
# the condition.

data2 = Pattern('-', data1)

# The condition that will warrant the second part after the '-'
# will be formed by just numbers but will not consume it.
# The below statement asserts that data0 will be built
# using the chars from data0 and data2 will be used
# to warrant the second part after the '-' will contain
# just numbers.
cond = ConsumeBack(data0, data2)

pattern = Pattern(cond)
pattern.test()

##############################################################################


from crocs import *

p0 = Seq('a', 'z')

# Fetch a random char.
c0 = Include(p0)

# Fetch one or more chars from c0.
data0 = Times(c0, 1)


# Define how the second part looks like.
data1 = Pattern('-', 'alpha')

# The condition that will warrant the second part after the '-'
# will be formed by just numbers but will not consume it.
# The below statement asserts that data0 will be built
# using the chars from data0 and data2 will be used
# to warrant the second part after the '-' will contain
# just numbers.
cond = ConsumeBack(data0, data1, neg=True)

pattern = Pattern(cond)
pattern.test()

##############################################################################
from crocs import *

# The string has digits in the beginning.
p0 = Seq('a', 'z')
c0 = Include(p0)
data = Pattern('alpha', Times(c0, 1))
data.hits()

# Set up the condition, it will match alpha only if it is not
# followed by beta.
cond = ConsumeBack('alpha', 'beta', neg=True)

# Finally set up the pattern.
pattern = Pattern(data0, cond)
pattern.test()
pattern.hits()
regx = search('[0-9]{1,}alpha(?!beta)', '3233alphaskljd')
regx.group(0)

regx = search('[0-9]{1,}alpha(?!beta)', '3233alphabeta')
regx.group(0)
from re import search
##############################################################################
from crocs import *

# 'abc1332abc90809KKKi82938HUAEHA8098shjkabc999alskjd989KK9283abc898'

from crocs import *

# Fetch one random char in 0-9.
c0 = Include(Seq('0', '9'))

# Get more random chars from c0.
fmt0 = Times(c0)

cond = ConsumeNext('abc', fmt0)
cond.test()
