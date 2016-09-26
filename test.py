Pre_set=set()
AS_set=set()
count=0
ascount=0
with open('./ribout.txt') as fi: 
	for line in fi:
		linecopy=line[0:len(line)-1]
		splits=linecopy.split(' ')
		prefix=splits[0]
		if not prefix in Pre_set:
			Pre_set.add(prefix)		
			count=count+1
		for AS in splits[1:len(splits)]:
			if not AS in AS_set:
				AS_set.add(AS)
				ascount=ascount+1

print 'unique prefixes: '+str(count)
print 'unique ASes:'+str(ascount)
