import collections
from collections import OrderedDict

CAIDA_FILE = './caidarel3.txt'
OUT_FILE='./cbgp_16bit_map.txt'
MAX_AS_NO=65535

mset=set()

with open(CAIDA_FILE) as fi:
	count=0
	for line in fi:
		ll=line[:len(line)-1]
		splits=ll.split(' ')
		one=splits[0]
		two=splits[1]
		one_i=int(one)
		two_i=int(two)
		if one_i>MAX_AS_NO:
			if not one in mset:
				mset.add(one)
				count=count+1

		if two_i>MAX_AS_NO:
			if not two in mset:
				mset.add(two)
				count=count+1
	print count