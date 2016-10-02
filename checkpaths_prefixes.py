# Check difference in 'provider' AS for different prefixes<Check done on rib file>

AS_PREFIXES='./AS_prefixes.txt'
RIBFILE='./ribout.txt'

#AS_PREFIXES='./tmppre.txt'
#RIBFILE='./tmprib.txt'

prefix_list=[] # save prefix list along their indexes
prefix_set=set()
list_set=[] # save provider etc. AS set corresponding to prefixes. Is a List of sets.

with open(AS_PREFIXES) as fi:
	for line in fi:
		ll=line[:len(line)-1]
		if not ll in prefix_set:
			prefix_set.add(ll)
			prefix_list.append(ll)
			list_set.append(set())




with open(RIBFILE) as fr:
	for line in fr:
		ll=line[:len(line)-1]
		splits=ll.split(' ')
		if splits[0] in prefix_set:
			idx = prefix_list.index(splits[0]) #index of set belonging to prefix.
			homeAS=splits[len(splits)-1]
			found_provider = False
			for AS in splits[len(splits)-2:0:-1]: #second last AS to second AS. leaving start AS
				mset=list_set[idx]
				if (AS!=homeAS) and (AS!=splits[1]):
					if (not AS in mset):
						print ll
						list_set[idx].add(AS)
					found_provider = True
				if found_provider:
					break


idx=0;
for S in list_set:
	print prefix_list[idx]
	print S
	idx=idx+1

fo=open('./provider_diff.txt', 'w')
plen =  len(prefix_list)
for i in range(0,plen):
	for j in range(0, plen):
		s1=list_set[i]
		s2=list_set[j]
		diff=s1.symmetric_difference(s2)
		fo.write(prefix_list[i]+': '+str(s1.__len__())+'    '+prefix_list[j]+':  '+str(s2.__len__())+'      '+str(diff.__len__())+'\n')
		print prefix_list[i]+': '+str(s1.__len__())+'    '+prefix_list[j]+':  '+str(s2.__len__())+'      '+str(diff.__len__())
