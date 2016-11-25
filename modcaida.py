
CAIDA_FILE='oldfin.txt'
mset=set()
with open(CAIDA_FILE) as fi:
	rels = fi.readlines()

for line in rels:
	ll=line[:len(line)-1]
	splits=ll.split(' ')
	mstr=splits[0]+':'+splits[1]
	set.add(mstr)

fo = open('oldout.txt', w)

for line in rels:
	ll=line[:len(line)-1]
	splits=ll.split(' ')
	rev = splits[1]+':'+splits[0]
	if not rev in mset: #reverse path not found in the set.
