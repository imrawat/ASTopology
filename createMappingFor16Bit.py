import collections
from collections import OrderedDict

CAIDA_FILE = './caidarel3.txt'
CAIDA_16BIT = './caida_16bit.txt'
OUT_FILE_1='./cbgp_16bit2AS_caida_map.txt'
OUT_FILE_2='./cbgp_AS216bit_caida_map.txt'
MAX_AS_NO=65535

temp_dict=dict()
AS_2_16bit_dict=dict()
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
				if not str(i) in temp_dict and not one in AS_2_16bit_dict:
					temp_dict[str(i)]=one
					AS_2_16bit_dict[one]=str(i)
					curr_idx=i+1
					print lnum
					break
			one_towrite=AS_2_16bit_dict[one]
		else:
			one_towrite=one
		if one_towrite=='-1':
			print '1 '+str(i)+' '+str(len(temp_dict))+' '+str(curr_idx)

		if two_i>MAX_AS_NO:
			for i in range(curr_idx, MAX_AS_NO+1):
				if not str(i) in temp_dict and not two in AS_2_16bit_dict:
					temp_dict[str(i)]=two
					AS_2_16bit_dict[two]=str(i)
					curr_idx=i+1
					print lnum
			two_towrite=AS_2_16bit_dict[two]
		else:
			two_towrite=two

		if two_towrite=='-1':
			print '2 '+str(i)+' '+str(len(temp_dict))+' '+str(curr_idx)

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


