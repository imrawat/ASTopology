"""
Gets all unique AS from caida file.
Used for getting a list of all ASes world over
"""

my_set=set()

CAIDA_FILE='./caidarel.txt'
OUT_FILE='all_as.txt'

with open(CAIDA_FILE) as fi:
	for line in fi:
		ll=line[:len(line)-1]
		splits=ll.split(' ')
		if not splits[0] in my_set:
			my_set.add(splits[0])
		if not splits[1] in my_set:
			my_set.add(splits[1])

count=0
with open(OUT_FILE, 'w') as fo:
	for key in my_set:
		count=count+1
		print str(count)+' '+key
		fo.write(key+'\n')
