# !/usr/bin/env python
# Name :  Madhur Rawat
# Organisation: IIIT Delhi
# Date : 22/06/17

import argparse

#Local imports
import constants

def get_network_boundary_impl(AS_FILE):
	CAIDAREL = constants.TEST_DATA + "caidarel.txt"
	print "CAIDAREL", CAIDAREL
	print "AS_FILE", AS_FILE

	as_set = set()
	fi = open(AS_FILE)
	for line in fi:
		line = line.strip()
		as_set.add(line[2:])

	boundary_set = set()
	fi = open(CAIDAREL)
	for line in fi:
		line = line.strip()
		splits = line.split()
		provider = splits[0]
		customer = splits[1]
		if (provider in as_set and not customer in as_set):
			boundary_set.add(provider)
		elif (customer in as_set and not provider in as_set):
			boundary_set.add(customer)
	return (boundary_set)
	fi.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Get country network boundary based on caida relations')
	parser.add_argument('-c', '--country_code', help='country code', required = True)

	args = parser.parse_args()
	COUNTRY_CODE = args.country_code

	
	AS_FILE = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_AS.txt"

	print get_network_boundary_impl(AS_FILE)

	

	
