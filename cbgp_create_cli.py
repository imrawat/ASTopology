''' cbgp_create_cli.py
	Create a .cli file for C-BGP which will load prefixes to AS and 
	use traceroute to get path from AS to a particular prefix.
	Uses alias as 16bit AS numbers
'''
import sys
import argparse
import commands

# Local imports
import constants
from checkForSameNetwork import get_network_for_prefix


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = 'create cli for country to country all to all')
	parser.add_argument('-c', '--country_code', help='create cli file all to all', required = True)
	parser.add_argument('-m', '--mode', help='convert to gao', required = True)
	parser.add_argument('-p', '--number_of_partitions', help='number of partitions for cli file', required = True)


	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	NO_OF_PARTITIONS = args.number_of_partitions
	MODE = args.mode

	if MODE == 'C' or MODE == "G2C" or MODE == "g2c" or MODE == "a2c" or MODE == "A2C":
		SUFFIX = "_ASPrefixes"
	elif MODE == 'T':
		SUFFIX = "_transport"
	elif MODE == "B":
		SUFFIX = "_bank"
	elif MODE == "G":
		SUFFIX = "_govt"
	elif MODE == "D":
		SUFFIX = "_dns"


	if not NO_OF_PARTITIONS.isdigit():
		print "Invalid number of partitions"
		exit()

	NO_OF_PARTITIONS = int(NO_OF_PARTITIONS)

	#File containing the AS number and its corresponding prefix to be added. This prefix will be the same which will be tracerouted.
	prefix_file = constants.TEST_DATA + COUNTRY_CODE + "/"+ COUNTRY_CODE + SUFFIX + ".txt"

	command = "cat " + prefix_file + " | wc -l"
	print 'command ', command
	num_prefixes = commands.getoutput(command)
	num_prefixes = int(num_prefixes)
	if NO_OF_PARTITIONS >= num_prefixes:
		max_prefix_per_cli = int(num_prefixes)
	else:
		max_prefix_per_cli = int(num_prefixes) / NO_OF_PARTITIONS


	#File containing the ASes from which traceroute will be done to prefixes
	as_list = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE +'_AS.txt'
	if MODE == "g2c" or MODE == "G2C":
		as_list = constants.TEST_DATA + "all_as.txt"
	elif MODE == "a2c" or MODE == "A2C":
		as_list = constants.TEST_DATA + "bgpranking.txt"

	#16bit mapped AS list
	CAIDA_REL_16BIT = 'caida_16bit.txt'

	#AS to its 16bit alias mapping.
	AS_TO_16BIT_MAPPING = constants.TEST_DATA + 'cbgp_AS216bit_caida_map.txt'	


	""" Save AS to 16bit mapping in a dict.
	"""
	mapping_dict=dict()
	with open(AS_TO_16BIT_MAPPING) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			splits=ll.split(' ')
			if not splits[0] in mapping_dict:
				mapping_dict[splits[0]]=splits[1]


	""" Add prefixes to CBGP routers. Router numbers are mapping of 
		actual AS numbers to 16bit aliases.
	"""

	for cli_file_num in range(0, NO_OF_PARTITIONS + 1):

		
		# cli file which will add prefixes to AS routers of the country 
		upto = (cli_file_num + 1) * max_prefix_per_cli
		
		if upto > num_prefixes:
			upto = num_prefixes
		ffrom = (cli_file_num * max_prefix_per_cli) + 1
		range_str = str(ffrom) + "to" + str(upto)
		if MODE == "C":			
			out_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + '_country_' + str(cli_file_num + 1)+ "_" + str(range_str) + '.cli'
		elif MODE == "G2C" or MODE == "g2c":
			out_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + '_g2c' + str(cli_file_num + 1)+ "_" + str(range_str) + '.cli'
		elif MODE == "a2c" or MODE == "A2C":
			out_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + '_a2c' + str(cli_file_num + 1)+ "_" + str(range_str) + '.cli'
		else:
			out_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + SUFFIX + "_" + str(cli_file_num + 1)+ "_" + str(range_str) + '.cli'

		fo = open(out_file, 'w')

		print 'prefix_file : '+prefix_file
		print 'AS list : '+as_list
		print 'out_file :'+out_file
		raw_input("Press key to continue....................")

		fo.write('bgp topology load --addr-sch=local \"'+CAIDA_REL_16BIT+'\"\n')
		fo.write('bgp topology install\n')
		fo.write('bgp topology policies\n')
		fo.write('bgp topology run\n')
		fo.write('sim run\n')

		prefix_set = set()
		network_set = set()

		line_num = 0
		with open(prefix_file) as fi:
			for line in fi:
				line_num = line_num + 1
				if line_num < ffrom:
					continue
				if line_num > upto:
					break
				ll = line.strip()
				splits=ll.split(' ')
				if MODE == "C" or MODE == "G2C" or MODE == "g2c" or MODE == "a2c" or MODE == "A2C":
					AS = splits[0]
					num=AS[2:]
					prefix = splits[1]
				else:
					num = splits[2]
					prefix = splits[3]

				if not num in mapping_dict:
					print num+' prefix AS not in caida'
					continue

				network = get_network_for_prefix(prefix)

				if network in network_set:
					print prefix, "network already exists"
					continue

				if not prefix in prefix_set: #should not be required after network check. but still...
					prefix_set.add(prefix)

				network_set.add(network)

				# add to mapped 16bit AS instead of actual AS numbers
				AS_16bit='AS'+mapping_dict[num]
				com = 'bgp router '+AS_16bit+' add network '+prefix
				# print com
				fo.write(com+'\n')
				fo.write('time save\n')
				fo.write('sim run\n')
				fo.write('print '+"\""+str(line_num)+' '+com+":\"   \n")
				fo.write('time diff   \n')
			
		print "len(prefix_set)", len(prefix_set)
		print "prefix_set", prefix_set
		print
		"""
		traceroute commands
		"""
		with open(as_list) as fi:
			for line in fi:
				ll=line.strip()
				if not MODE == "a2c" or MODE == "A2C":
					num=ll[2:]
				else: 
					splits = ll.split()
					num = splits[0]
				if not num in mapping_dict:
					print num+' AS not in caida'
					continue
				AS_16bit='AS'+mapping_dict[num]
				for prefix in prefix_set:
					com = 'bgp router '+AS_16bit+' record-route '+prefix
					# print com
					fo.write(com+'\n') 		


