# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization: IIIT Delhi
# Date : 16/6/17

import random
import socket
import struct
import argparse

import constants

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Generate random prefixes for country. Only if AS has announced prefixes')
	parser.add_argument('-c', '--country_code', help='Country code', required = True)
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	as_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_AS.txt"
	announced_prefixes = constants.TEST_DATA + "announced_prefixes.txt"
	out_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_ASPrefixes.txt"
	
	print "as_file", as_file
	print "announced_prefixes", announced_prefixes
	print "out_file", out_file

	fi_as = open(as_file)
	fi_announced = open(announced_prefixes)
	fo = open(out_file, "w")

	as_having_announced_prefix = set()
	for line in fi_announced:
		line = line.strip()
		splits = line.split()
		if int(splits[1]) > 0:
			as_having_announced_prefix.add(splits[0])

	generated_prefixes = set()
	for i, line in enumerate(fi_as):
		done = False
		AS = line.strip()
		if not AS in as_having_announced_prefix:
			
			continue

		while(not done):
			prefix = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
			prefix = prefix + "/32"
			if not prefix in generated_prefixes:
				line_to_write = AS + " " + prefix
				print line_to_write
				fo.write(line_to_write + "\n")
				done = True
	fo.close()


	