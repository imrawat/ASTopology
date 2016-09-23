AS_set=set()
#read all AS of egpyt and store them in a set
with open('./EgyptASwoRank.txt') as fa:
        aslist=fa.readlines()
for line in aslist:
        AS=line[0:len(line)-1]
        AS_set.add(AS[2:])
fa.close()


StartAS_set=set();
f=open('./startAS.txt', 'w')
with open('./prefix_ribpath.txt') as pfo:
	for line in pfo:
		splits=line.split(' ')
#		print splits[1]
#		f.write(splits[1]+'\n')
		if not splits[1] in StartAS_set:
			StartAS_set.add(splits[1])
		if splits[1] in AS_set:
			print 'there it is'

for startAS in StartAS_set:
	f.write(startAS+'\n')
#	print startAS
f.close()

with open('./AllStartAS.txt') as fa:
	for line in fa:
		AS = line[0:len(line)-1]
		if AS in AS_set:
			print AS
