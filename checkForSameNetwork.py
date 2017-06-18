# !/usr/bin/env python
# Name :  Madhur Rawat
# Organisation: IIIT Delhi
# Date : 16/06/17

import argparse

#local imports	
import constants


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Check prefixes list for same prefix. Else CBGP gives error')
	parser.add_argument('-c', '--country_code', help='country code', required = True)
	parser.add_argument('-m', '--mode', help='all ot imp', required = True)
	
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	MODE = args.mode

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

	INFILE = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + SUFFIX +".txt"
	print 'INFILE', INFILE
	print

	networkdict = dict()
	with open(INFILE) as fi:
		for line in fi:
			line = line.strip()
			if not line[0] == "#":
				splits = line.split()
				if not MODE == "C":
					AS = splits[2]
					ip = splits[1]
					mask = 32
				else:
					AS = splits[0]
					prefix = splits[1]
					prefsplits = prefix.split("/")
					if len(prefsplits) < 2:
						print line + " len(prefsplits) " + str(len(prefsplits)) 
						continue
					mask = prefsplits[1]
					mask = int(mask)
					ip = prefsplits[0]
				ipsplits = ip.split(".")
				if len(ipsplits) < 4:
					print line + " len(ipsplits) " + str(len(ipsplits)) 
					continue
				network = ""
				for d in ipsplits:
					b = bin(int(d))
					b = b[2:]
					while(len(b) < 8):
						b = "0" + b
					network = network + b
				network = network[:mask]
				if network in networkdict:
					networkdict[network].append(AS)
				else:
					ASlist = [AS]
					networkdict[network] = ASlist

	fi.close()
	for network in networkdict:
		print network, networkdict[network]
