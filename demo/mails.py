from crocs.regex import Seq, Include, Repeat, Pattern, NamedGroup, Include

# First we define how our Patterns look like.
name_letters = Include(Seq('a', 'z'))

# The regex {n,m} repeatition. The name should contains more
# than 0 chars.
name = Repeat(name_letters, 1)

# Create a named group to make it available after matching.
name = NamedGroup('name', name)

# The hostname part looks like the name except
# it starts with 'python' in the beginning, 
hostname = Repeat(name_letters, 1)
hostname = NamedGroup('hostname', 'python', hostname)

# The Pattern class joins the sub patterns it forms a single one.
mail = Pattern(name, '@', hostname, '.', 'br')
mail.test()
mail.hits()
