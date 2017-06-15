import os
import time
import argparse
import subprocess
import time
import collections
import constants
from collections import OrderedDict

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Analysis of ASes of dns reolvers\'s')
	parser.add_argument('-c', '--country_code', help='country_code of dns resolver file', required = True)

	args = parser.parse_args()
	COUNTRY_CODE = args.country_code

	in_file = constants.TEST_DATA + "dns_resolvers_" + COUNTRY_CODE + ".csv"
	out_file = constants.TEST_DATA + COUNTRY_CODE + "_dns.txt"
	print "in_file " + in_file
	print "out_file", out_file
	fo = open(out_file, "w")

	as_dict = dict()
	sorted_as_dict = OrderedDict()

	with open(in_file) as fi:
		curr_line = 0
		
		for line in fi:
			curr_line = curr_line + 1
			if curr_line > 1:
				line = line.strip()
				splits = line.split(",")
				as_num = splits[4]
				routed_prefix = splits[5]
				as_name = splits[6]
				as_name = as_name.replace(" ", "_")
				print as_name
				if as_num in as_dict:
					t_list = as_dict[as_num]
					if not (routed_prefix, as_name) in t_list:
						t_list.append((routed_prefix, as_name))
				else:
					t_list = []
					t_list.append((routed_prefix, as_name))
					as_dict[as_num] = t_list

	sorted_as_dict = collections.OrderedDict(sorted(as_dict.items()))

	for key, val in sorted_as_dict.iteritems():
		line_to_write = val[0][1] + " " + val[0][0] + " " + key + " " + str(len(val))
		print line_to_write
		fo.write(line_to_write + "\n")

