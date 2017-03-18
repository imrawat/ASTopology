"""
this program reads a list of ASes in AS_FILE and path from finalpaths<gao's paths>
for each path in RAW_RIB it finds for first occurance of any AS in AS_FILE.
If found it construct a path from that AS to each home prefix.
Duplicate paths or duplicate ASes within a path are handled(only unique)
Finally it calculates the no of prefixes to which an AS has a path(sinle/multiple)(total)
and the no of prefixes to which an AS has multiple paths(multiple)
"""

from collections import OrderedDict
# 41.128.214.0/24 6 3 169 6127 24863 6762 3216 12695 59498 
AS_FILE='./all_as.txt'
RAW_RIB='./finalpaths.txt'
OUT_FILE='./gaocheckfinalout.txt'

asset=set()

with open(AS_FILE) as fa:
	for AS in fa:
		asset.add(AS.strip())

print asset
path_set=set()
zero_path_set=set()
line_num=0
with open(RAW_RIB) as fi:
	for line in fi:
		line_num=line_num+1
		ll=line[:len(line)-1]
		splits=ll.split(' ')
		lastAS = splits[4]
		for AS in splits[len(splits):4:-1]:
			if AS in asset and AS!=lastAS:
				#store path from here onwards in a set. ASes in this path should be unique.
				startidx = splits.index(AS)
				lastidx=3 #iterate uptil last index backwards
				temp_dict=OrderedDict()
				for index in range(startidx, lastidx, -1):
					if not splits[index] in temp_dict:
						temp_dict[splits[index]]=1

				hkey=''
				for key in temp_dict:
					hkey=hkey+':'+key
				hkey=hkey[1:]+':'+splits[0] #a unique path starting with one of the required starting AS is found.
				if not hkey in path_set:
					print str(line_num)+' '+hkey
					path_set.add(hkey)

	# print 
	# for key in path_set:
	# 	print key
print

my_dict=dict()

for key in path_set:
	splits=key.split(':')
	startAS=splits[0]
	prefix=splits[len(splits)-1]
	new_key=startAS+':'+prefix
	if not new_key in my_dict:
		my_dict[new_key]=1
	else:
		my_dict[new_key]=my_dict[new_key]+1


total_dict=dict()
multiple_dict=dict()
allmultiple=0
alltotal=0
for key in my_dict:
		splits=key.split(':')
		startAS=splits[0]
		if not startAS in total_dict:
			total_dict[startAS]=1
		else:
			total_dict[startAS]=total_dict[startAS]+1
		if my_dict[key]>1:
			if not startAS in multiple_dict:
				multiple_dict[startAS]=1
			else:
				multiple_dict[startAS]=multiple_dict[startAS]+1
			allmultiple=allmultiple+1
		alltotal=alltotal+1



with open(OUT_FILE, 'w') as fo:
	for AS in asset:
		
		
		if AS in total_dict:
			print '------------------------------------------'
			fo.write('------------------------------------------\n')
			print 'AS : '+AS
			fo.write('AS : '+AS+'\n')
			print 'total='+str(total_dict[AS])
			fo.write('total='+str(total_dict[AS])+'\n')
			if AS in multiple_dict:
				print 'multiple='+str(multiple_dict[AS])
				fo.write('multiple='+str(multiple_dict[AS])+'\n')
				print 'mult% = '+str((float(multiple_dict[AS])/float(total_dict[AS]))*100)+'%'
				fo.write('mult% = '+str((float(multiple_dict[AS])/float(total_dict[AS]))*100)+'%\n')
		else:
			if not AS in zero_path_set:
				zero_path_set.add(AS)

	print
	print '*****************************************************'
	print 'all total : '+str(alltotal)
	fo.write('all total : '+str(alltotal)+'\n')
	print 'all multiple : '+str(allmultiple)
	fo.write('all multiple : '+str(allmultiple)+'\n')
	if alltotal!=0:
		print 'all mult% = '+str((float(allmultiple)/float(alltotal))*100)+'%'
		fo.write('all mult% = '+str((float(allmultiple)/float(alltotal))*100)+'%\n')

	print '*****************************************************'
	print 'ASes with zero path'
	zero_count=0
	for key in zero_path_set:
		zero_count=zero_count+1
		print str(zero_count)+' '+key
		fo.write(str(zero_count)+' '+key+'\n')

