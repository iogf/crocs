from crocs.regex import Seq, Include, Repeat, Pattern, NamedGroup, Include

# First we define how our Patterns look like.
name_letters = Seq('a', 'z')
name_numbers = Seq('0', '9')
name_signs   = '_.-'

# Describe the chars in the name part..
name_chars = Include(name_letters, name_numbers, name_signs)

# The regex {n,m} repeatition.
name = Repeat(name_chars, 1)

# The first letter in the mail name has to be a in 'a-z'.
name = Pattern(Include(name_letters), name)

# Create a named group to make it available after matching.
name = NamedGroup('name', name)

# The random's hostname part looks like the name except
# it starts with 'python' in the beginning, 
hostname_chars = Include(name_letters)
hostname = Repeat(hostname_chars, 1)

# Keep reference for hostname to make its value 
# available after matching.
hostname = NamedGroup('hostname', 'python', hostname)

# Finally we generate the regex and check how it looks like.
match_mail = Pattern(name, '@', hostname, '.', 'br')
match_mail.test()
match_mail.hits()
