# !/usr/bin/env python
# Name :  Madhur Rawat
# Organisation: IIIT Delhi
# Date : 22/06/17

import argparse

#Local imports
import constants

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Get country network boundary based on caida relations')
	parser.add_argument('-c', '--country_code', help='country code', required = True)

	args = parser.parse_args()
	COUNTRY_CODE = args.country_code

	CAIDAREL = constants.TEST_DATA + "caidarel.txt"
	AS_FILE = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_AS.txt"

	print "CAIDAREL", CAIDAREL
	print "AS_FILE", AS_FILE

	as_set = set()
	fi = open(AS_FILE)
	for line in fi:
		line = line.strip()
		as_set.add(line[2:])
	print "len(as_set)", len(as_set)

	boundary_set = set()
	fi = open(CAIDAREL)
	for line in fi:
		line = line.strip()
		splits = line.split()
		provider = splits[0]
		customer = splits[1]
		# print '(provider in as_set and not customer in as_set)', (provider in as_set and not customer in as_set)
		# print '(customer in as_set and not provider in as_set)', (customer in as_set and not provider in as_set)
		if (provider in as_set and not customer in as_set):
			# print '1', line
			boundary_set.add(provider)
		elif (customer in as_set and not provider in as_set):
			# print '2', line
			boundary_set.add(customer)
	print "len(boundary_set)", len(boundary_set)
	print boundary_set
	fi.close()
