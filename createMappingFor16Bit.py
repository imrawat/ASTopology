import collections
from collections import OrderedDict

CAIDA_FILE = './caidarel3.txt'
CAIDA_16BIT = './caida_16bit.txt'
OUT_FILE_1='./cbgp_16bit2AS_caida_map.txt'
OUT_FILE_2='./cbgp_AS216bit_caida_map.txt'
MAX_AS_NO=65536

temp_dict=dict()
mapping_dict=OrderedDict()

curr_idx=1

f16=open(CAIDA_16BIT, 'w')

with open(CAIDA_FILE) as fi:
	for line in fi:
		ll=line[:len(line)-1]
		splits=ll.split(' ')
		one=splits[0]
		two=splits[1]
		one_i=int(one)
		two_i=int(two)
		if one_i<=MAX_AS_NO:
			if not one in temp_dict:
				temp_dict[one]=one
				
		if two_i<=MAX_AS_NO:
			if not two in temp_dict:
				temp_dict[two]=two


added_as_set=set()

with open(CAIDA_FILE) as fi:
	lnum=0
	for line in fi:
		lnum=lnum+1
		ll=line[:len(line)-1]
		splits=ll.split(' ')
		one=splits[0]
		two=splits[1]
		one_i=int(one)
		two_i=int(two)

		one_towrite='-1'
		two_towrite='-1'
		three_towrite=splits[2]

		if one_i>MAX_AS_NO:
			for i in range(curr_idx, MAX_AS_NO+1):
				done=False
				if not str(i) in temp_dict and not one in added_as_set:
					temp_dict[str(i)]=one
					added_as_set.add(one)
					curr_idx=i+1
#					print lnum
					done=True
				if done==True:
					one_towrite=str(i)
					break
		else:
			one_towrite=one

		if two_i>MAX_AS_NO:
			for i in range(curr_idx, MAX_AS_NO+1):
				done=False
				if not str(i) in temp_dict and not two in added_as_set:
					temp_dict[str(i)]=two
					added_as_set.add(two)
					curr_idx=i+1
					two_towrite=str(i)
#					print lnum
					done=True
				if done==True:
					two_towrite=str(i)
					break
		else:
			two_towrite=two
		if one_towrite=='-1' or two_towrite=='-1':
			print '* '+ll
		f16.write(one_towrite+' '+two_towrite+' '+three_towrite+'\n')

mapping_dict = collections.OrderedDict(sorted(temp_dict.items()))

print OUT_FILE_1
print OUT_FILE_2
print CAIDA_16BIT
fo1=open(OUT_FILE_1, 'w')
fo2=open(OUT_FILE_2, 'w')
try:
	for key in mapping_dict:
		print key+' '+mapping_dict[key]
		fo1.write(key+' '+mapping_dict[key]+'\n')
		fo2.write(mapping_dict[key]+' '+key+'\n')
finally:
	fo1.close()
	fo2.close()
	f16.close()


