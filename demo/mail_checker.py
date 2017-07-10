"""
It solves the problem of catching mails whose domain contains 
'br' in the beginning and the hostname contains 'python' in  the beginning too. 
It makes sure that the first letter in the mail name is in the set a-z as well.
"""

from crocs import *

# First we define how our patterns look like.
name_valid_letters = Seq('a', 'z')
name_valid_numbers = Seq('0', '9')
name_valid_signs   = '_.-'

# The include works sort of Times except for one char. 
# You can think of it as fetching one from the described sets.
name_valid_chars = Include(name_valid_letters, 
name_valid_numbers, name_valid_signs)

# Think of the Times class as meaning: fetch the
# described patterns one or more times.
name_chunk = Times(name_valid_chars, 1)

# The first letter in the mail name has to be a in 'a-z'.
name_fmt = Pattern(Include(name_valid_letters), name_chunk)

# Think of group as a way to keep reference
# to the fetched chunk.
name = NamedGroup('name', name_fmt)

# The random's hostname part looks like the name except
# it starts with 'python' in the beginning, 
# so we fetch the random chars.
hostname_chars = Include(name_valid_letters)
hostname_chunk = Times(hostname_chars, 1)

# We format finally the complete hostname pattern.
hostname_fmt = Pattern('python', hostname_chunk)

# Keep reference for the group.
hostname = NamedGroup('hostname', hostname_fmt)

# Define the domain format.
domain_fmt = Pattern('br', Include(name_valid_letters))

# Keep reference of the domain chunk.
domain  = NamedGroup('domain', domain_fmt)

# Finally we generate the regex and check how it looks like.
match_mail = Pattern(name, '@', hostname, '.', domain)
match_mail.test()







