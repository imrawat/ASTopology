# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization: IIIT Delhi
# Date : 30/12/16

""" Convert CBGP traceroute paths to GAO output 
	format paths. Mapping is reverted back during conversion.

	CBGP format: 0.0.27.106 130.104.0.0/16 SUCCESS 7018 3303 2611 <where 7018 is start AS and 2611 is home AS consisting of destination prefix>
	GAO format: 130.104.0.0/16 2611 3303 7018
"""

import argparse

#local imports
import constants

def get_mapping_dict(BIT16_TO_AS_MAPPING) :
	"""Save 16bit to AS mapping in a dict.
	"""
	mapping_dict=dict()
	with open(BIT16_TO_AS_MAPPING) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			splits=ll.split(' ')
			if not splits[0] in mapping_dict:
				mapping_dict[splits[0]]=splits[1]
	return mapping_dict


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'convert cbgp traceroute paths to gao format')
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

	AS_FILE = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_AS.txt"

	BIT16_TO_AS_MAPPING = constants.TEST_DATA + 'cbgp_16bit2AS_caida_map.txt'
	mapping_dict = get_mapping_dict(BIT16_TO_AS_MAPPING)

	all_country_as = set()
	with open(AS_FILE) as fi:
		for line in fi:
			line = line.strip()
			country_AS = line[2:]
			if not country_AS in all_country_as:
				all_country_as.add(country_AS)

	#File having CBGP format traceroute paths
	in_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_cbgp_trace" + SUFFIX + ".txt"
	# in_file = "/Users/Madhur/Google_Drive/Thesis_Mtech/Test_Data/IL/temp.txt"
	out_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_gao_cbgp_paths" + SUFFIX + ".txt"
	out_file_including_outside = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_gao_cbgp_paths" + SUFFIX_INCLUDING_OUTSIDE + ".txt"

	print 'in_file', in_file
	print 'out_file', out_file
	print 'out_file_including_outside', out_file_including_outside

	fo=open(out_file, 'w')
	foio = open(out_file_including_outside, 'w')

	with open(in_file) as fi:
		line_num = 0
		for line in fi:
			ll=line.strip()
			line_num = line_num + 1
			
			splits=ll.split()
			print line_num
			if splits[2]=='UNREACHABLE':
				print ll
				continue

			prefix = splits[1]	
			line_to_write = prefix
			line_to_write_including_outside = prefix
			for idx in range(len(splits) - 1, 2, -1):
				if mapping_dict[splits[idx]] in all_country_as:
					line_to_write = line_to_write + " " + mapping_dict[splits[idx]]
				line_to_write_including_outside = line_to_write_including_outside + " " + mapping_dict[splits[idx]]
			line_to_write = line_to_write + "\n"
			line_to_write_including_outside = line_to_write_including_outside + "\n"
			# print line_to_write
			# print line_to_write_including_outside
			fo.write(line_to_write)
			foio.write(line_to_write_including_outside)

	fo.close()
