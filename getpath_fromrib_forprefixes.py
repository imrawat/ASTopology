#Get all path for prefixes in list from rib out file(ribout.txt)

prefix_set=set()
StartAS_set=set()

#read all prefixes of all ASes within Egypt and prepare a set from them
with open('./prefixlist_EG_all.txt') as fpi:
	prefixes=fpi.readlines()
for line in prefixes:
	prefix=line[0:len(line)-1]
	if(prefix[0:3] != '***'):
		if not prefix in prefix_set:
			prefix_set.add(prefix)
fpi.close()

AS_set=set()
#read all AS of egpyt and store them in a set
with open('./EgyptASwoRank.txt') as fa:
        aslist=fa.readlines()
for line in aslist:
        AS=line[0:len(line)-1]
        AS_set.add(AS[2:])
fa.close()


fo=open('./prefix_ribpath.txt', 'w')
key=''

with open('./ribout.txt') as fi: 
        for line in fi:
		splits=line.split(' ')
		prefix=splits[0]
		AS=splits[1]
		if prefix in prefix_set: #prefix is an EG prefix
			idx=1
			for AS in splits[1:len(splits)-1]: 
				if AS in AS_set: #path other than home AS has an EG AS.
					#check if remaining AS are also same as this AS
					print line+'   :   '+AS+' '+str(idx)
					fo.write(line)
					break
				idx=idx+1		
fo.close()
fi.close()
