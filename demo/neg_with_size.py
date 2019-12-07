from crocs import Pattern, ConsumeBack, Include, Size, ConsumeNext

# It will consume abc only if it is not followed by aaa.
c = Include('aum')
e1 = Pattern(ConsumeBack('abc', Size(c, 3, 6), neg=True))
e1.test()

c = Include('aum')
e2 = Pattern(ConsumeNext('abc', Size(c, 3, 6), neg=True))
e2.test()




