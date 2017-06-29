# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization: IIIT Delhi
# Date : 28/06/16

import sys
sys.path.append('./finding_min_cut')
import argparse
import math
import collections
import operator
from collections import OrderedDict

#local imports
import constants
from get_network_boundary import get_network_boundary_impl

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Check ')
	parser.add_argument('-c', '--country_code', help='convert to gao', required = True)
	parser.add_argument('-m', '--mode', help='convert to gao', required = True)
	
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	MODE = args.mode

	if MODE == 'C':
		SUFFIX = "_country_all"
		SUFFIX_INCLUDING_OUTSIDE = "_country_all_including_outside"
	elif MODE == 'T':
		SUFFIX = "_imp_transport"
		SUFFIX_INCLUDING_OUTSIDE = "_imp_transport_including_outside"
	elif MODE == "B":
		SUFFIX = "_imp_bank"
		SUFFIX_INCLUDING_OUTSIDE = "_imp_bank_including_outside"
	elif MODE == "G":
		SUFFIX = "_imp_govt"
		SUFFIX_INCLUDING_OUTSIDE = "_imp_govt_including_outside"
	elif MODE == "D":
		SUFFIX = "_imp_dns"
		SUFFIX_INCLUDING_OUTSIDE = "_imp_dns_including_outside"
	elif MODE == "G2C" or MODE == "g2c":
		SUFFIX = "_g2c"
		SUFFIX_INCLUDING_OUTSIDE = "_g2c_including_outside"
	elif MODE == "A2C" or MODE == "a2c":
		SUFFIX = "_a2c"
		SUFFIX_INCLUDING_OUTSIDE = "_a2c_including_outside"

	PATH_FILE = out_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_gao_cbgp_paths" + SUFFIX + ".txt"
	AS_FILE = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_AS.txt"
	network_boundary = get_network_boundary_impl(AS_FILE)

	fi = open(PATH_FILE)
	max_hops = float('-inf')
	min_hops = float('inf')
	mean = 0.0;
	median_list = []
	mode_dict = dict()
	total = 0.0
	count = 0
	for line in fi:
		line = line.strip()
		splits = line.split()
		if len(splits) > 3: #atleast one hop path
			if (not splits[len(splits) - 1] in network_boundary) and (splits[1] in network_boundary):
				count = count + 1
				hops = len(splits) - 2
				if hops > max_hops:
					max_hops = hops
				if hops < min_hops:
					min_hops = hops
				if not hops in mode_dict:
					mode_dict[hops] = 1.0
				else:
					mode_dict[hops] = mode_dict[hops] + 1.0
				median_list.append(hops)
				total = total + hops
	print COUNTRY_CODE
	print 'total paths from inner to network_boundary', total
	print 'max_hops', max_hops
	print 'min_hops', min_hops
	ordered_mode_dict = collections.OrderedDict(sorted(mode_dict.items(), key=operator.itemgetter(1), reverse = True))
	print 'mode', list(ordered_mode_dict)[0]
	sorted_median_list = sorted(median_list)
	x = len(sorted_median_list)
	if x%2 == 0:
		median = (sorted_median_list[x/2] + sorted_median_list[(x/2)+1])/2
		print 'median', median
	else:
		median = sorted_median_list[(x/2)+1]
		print 'median', median
	print 'mean', (total/count)
	print '*' * 50







