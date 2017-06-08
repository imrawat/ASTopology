import itertools
l = [100,90,80,70,60,50]

c = itertools.combinations(l, 3)
for cc in c:
	sum = 0
	for ccc in cc:
		sum = sum + ccc
	print cc, sum
