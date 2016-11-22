"""
this program reads a list of ASes in AS_FILE and raw rib file from RAW_RIB
for each path in RAW_RIB it finds for first occurance of any AS in AS_FILE.
If found it construct a path from that AS to each home prefix.
Duplicate paths or duplicate ASes within a path are handled(only unique)
Finally it calculates the no of prefixes to which an AS has a path(sinle/multiple)(total)
and the no of prefixes to which an AS has multiple paths(multiple)
"""

from collections import OrderedDict
#1.23.128.0/24 3130 1239 1239 1239 6453 9498 9498 3232 4552 4552 4552
AS_FILE='./all_as.txt'
RAW_RIB='./ribout.txt'
OUT_FILE='./gaocheckout.txt'

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
		lastAS = splits[len(splits)-1]
		done=False; #to break when we began creating a path after finding an start as.
		for AS in splits[1:]:
			if AS in asset and AS!=lastAS:
				#store path from here onwards in a set. ASes in this path should be unique.
				startidx = splits.index(AS)
				done=True;
				lastidx=len(splits) #iterate uptil last index
				temp_dict=OrderedDict()
				for index in range(startidx, lastidx):
					if not splits[index] in temp_dict:
						temp_dict[splits[index]]=1

				hkey=''
				for key in temp_dict:
					hkey=hkey+':'+key
				hkey=hkey[1:]+':'+splits[0] #a unique path starting with one of the required starting AS is found.
				if not hkey in path_set:
					print str(line_num)+' '+ll
					path_set.add(hkey)
			if done:
				break

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

with open(OUT_FILE, 'w') as fo:
	alltotal=0
	allmultiple=0
	for AS in asset:
		total=0
		multiple=0
		for key in my_dict:
			splits=key.split(':')
			if splits[0]==AS:
				if my_dict[key]>1:
					multiple=multiple+1
					allmultiple=allmultiple+1
				total=total+1
				alltotal=alltotal+1
		print '------------------------------------------'
		fo.write('------------------------------------------\n')
		print 'AS : '+AS
		fo.write('AS : '+AS+'\n')
		print 'total='+str(total)
		fo.write('total='+str(total)+'\n')
		print 'multiple='+str(multiple)
		fo.write('multiple='+str(multiple)+'\n')
		if total>0:
			print 'mult% = '+str((float(multiple)/float(total))*100)+'%'
			fo.write('mult% = '+str((float(multiple)/float(total))*100)+'%\n')
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
