# !/usr/bin/env python
# Name :  Madhur Rawat
# Organisation: IIIT Delhi
# Date : 16/06/17

import os
import time
import commands
import argparse

#local imports
import constants

'''
For important destinations like banks,
get IP address and IP to AS mapping
'''

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Get IP or AS for website. For Bank,Govt,Transport. NOT for dns')
	parser.add_argument('-c', '--country_code', help='country code', required = True)
	parser.add_argument('-m', '--mode', help='Country(C), Bank(B), Govt(G), DNS(D)', required = True)
	parser.add_argument('-t', '--type', help='get IP(I) or AS mapping(A)', required = True)
	
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	MODE = args.mode
	TYPE = args.type

	if MODE == 'C':
		SUFFIX = "_ASPrefixes"
	elif MODE == 'T':
		SUFFIX = "_transport"
	elif MODE == "B":
		SUFFIX = "_bank"
	elif MODE == "G":
		SUFFIX = "_govt"
	elif MODE == "D":
		SUFFIX = "_dns"


	in_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + SUFFIX +".txt"
	print 'INFILE', in_file


	with open(in_file) as fi:
		for line in fi:
			line = line.strip()
			# Neglect lines starting with #
			# They may be AS with existing prefixes
			if not line[0] == "#":
				splits = line.split()
				if TYPE == "A":
					if len(splits) > 1:
						command = "whois -h whois.cymru.com \" -v " + splits[1] + "\""
						result = commands.getoutput(command)
						asline = result.split("\n")[1]
						aslinesplits =  asline.split("|")
						AS = aslinesplits[0].strip()
						bgp_prefix = aslinesplits[2].strip()
						print splits[0], splits[1], AS, bgp_prefix
				elif TYPE == "I":
					command = "dig " + splits[0] + " 8.8.8.8 +short"
					result = commands.getoutput(command)
					print splits[0], result

				time.sleep(1)