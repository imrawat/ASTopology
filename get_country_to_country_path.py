# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization: IIIT Delhi
# Date : 15/12/16
''' Get path from finalpaths.txt
	Path from an AS within Egypt to Egypt Prefix.
	Such an AS can be start or intermediatry AS.
'''

import argparse
from collections import OrderedDict

#local imports
import constants

if __name__  ==  "__main__":
	parser  =  argparse.ArgumentParser(description  =  'Get paths from list of paths within country')
	parser.add_argument('-c', '--country_code', help = 'country code', required  =  True)
	parser.add_argument('-m', '--mode', help = 'G:Gao C:cbgp', required  =  True)

	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	MODE = args.mode




	if MODE == "C":
		IS_CAIDA = True
	elif MODE == "G":
		IS_CAIDA = False
	else:
		print 'Invalid mode value'
		exit()

	if IS_CAIDA:
		print "*** CAIDA is Enabled ***"
	COUNTRY_AS_LIST = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + '_AS.txt'
	print 'COUNTRY_AS_LIST : ' + COUNTRY_AS_LIST

	PATH_FILE = constants.TEST_DATA + COUNTRY_CODE + "/" + 'finalpaths.txt'
	if IS_CAIDA:
		PATH_FILE = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + '_gao_cbgp_paths.txt'
	print 'PATH_FILE : ' + PATH_FILE

	OUT_FILE = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + '2' + COUNTRY_CODE + '_finalpaths.txt'
	if IS_CAIDA:
		OUT_FILE = 'cbgp' + OUT_FILE
	print 'OUT_FILE : ' + OUT_FILE

	print 

	as_set = set()
	with open(COUNTRY_AS_LIST) as fi:
		for line in fi:
			line  =  line.strip()
			AS = line[2:]
			if not AS in as_set:
				as_set.add(AS)


	fo = open(OUT_FILE, 'w')

	prefix_set = set()
	with open(PATH_FILE) as f2:
		for line in f2:
			ll = line.strip()
			splits = ll.split()
			ASidx = len(splits)-1
			homeProviderIdx = 5
			prefix_set.add(splits[0])
			if IS_CAIDA:
				homeProviderIdx = 2

			# set of AS found in current path.
			as_found_in_current_path = set()

			homeIdx = 4

			if IS_CAIDA:
				homeIdx = 1
		
			for idx in range(len(splits) - 1, homeIdx, -1):
				AS = splits[idx]
				if AS in as_set and AS != splits[homeIdx] and not AS in as_found_in_current_path:
					path_parts = []
					as_found_in_current_path.add(AS)
					for in_idx in range(0, idx + 1):
						if (splits[in_idx] not in path_parts) and (not IS_CAIDA and (not in_idx in [1 ,2 ,3])):
							if splits[in_idx] in as_set or in_idx in [0, homeIdx]:
								path_parts.append(splits[in_idx])
					line_to_write = ""
					for part in path_parts:
						line_to_write = line_to_write + " " + part
					line_to_write = line_to_write[1:]
					print 'original path', ll
					print line_to_write
					fo.write(line_to_write + "\n")


