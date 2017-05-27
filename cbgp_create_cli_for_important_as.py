"""
Create a .cli file for C-BGP which will load prefixes to AS and 
use traceroute to get path from AS to a particular prefix.
Uses alias as 16bit AS numbers
"""

import sys
import argparse

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = 'find cut for defender in directed graph')
	parser.add_argument('-c', '--country_code', help='Find Cut Directed', required = True)
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	print "Since important target prefixes are smaller in number we donot get paths in batches."
	print "Fetch in batches is done for all to all mappings only."
	domains = ['bank', 'govt', 'transport']
	print "domains " + str(domains)
	print "options " + str(range(1, len(domains) + 1))

	selected_imp = raw_input("Enter space separated choice. Currently single choice only ")
	if not selected_imp.isdigit() or (int(selected_imp) - 1) > (len(domains) - 1):
		print "invalid selected_imp " + selected_imp
		exit()

	#File containing the ASes from which traceroute will be done to prefixes
	as_list = './'+COUNTRY_CODE+'_AS.txt'

	#16bit mapped AS list
	CAIDA_REL_16BIT='./caida_16bit.txt'

	#AS to its 16bit alias mapping.
	AS_TO_16BIT_MAPPING='./cbgp_AS216bit_caida_map.txt'

	# cli file which will add prefixes to AS routers of the country 
	out_file='./'+COUNTRY_CODE+'_imp'
	out_file = out_file + "_" + domains[int(selected_imp)-1]
	out_file = out_file + ".cli"

	fo = open(out_file, 'w')

	print 'AS list : '+as_list
	print 'out_file :'+out_file

	fo.write('bgp topology load --addr-sch=local \"'+CAIDA_REL_16BIT+'\"\n')
	fo.write('bgp topology install\n')
	fo.write('bgp topology policies\n')
	fo.write('bgp topology run\n')
	fo.write('sim run\n')

	prefix_set = set()


	"""
	Save AS to 16bit mapping in a dict.
	mapping_dict[actual_AS] = alias_AS
	"""
	mapping_dict=dict()
	with open(AS_TO_16BIT_MAPPING) as fi:
		for line in fi:
			ll=line.strip()
			splits=ll.split(' ')
			if not splits[0] in mapping_dict:
				mapping_dict[splits[0]]=splits[1]


	"""
	add prefixes to CBGP routers. Router numbers are mapping of 
	actual AS numbers to 16bit aliases.
	"""

	count=1


	important_prefix_files = []
	domain = domains[int(selected_imp) - 1]
	prefix_file = './'+COUNTRY_CODE+'_'+domain+'.txt'

	print "perfix file : "+prefix_file
	with open(prefix_file) as fi:
		for line in fi:
			ll=line.strip()
			if ll[0] == "#":
				continue
			splits=ll.split(' ')
			num = splits[2]
			prefix = splits[1]

			if not num in mapping_dict:
				print num+' not in caida'
				continue

			if not prefix in prefix_set:
				prefix_set.add(prefix)

			# add to mapped 16bit AS instead of actual AS numbers
			AS_16bit='AS'+mapping_dict[num]
			prefix = prefix+'/32'
			com = 'bgp router '+AS_16bit+' add network '+prefix
			# print com
			fo.write(com+'\n')
			fo.write('time save\n')
			fo.write('sim run\n')
			fo.write('print '+"\""+str(count)+' '+com+":\"   \n")
			fo.write('time diff   \n')
			count=count+1



	print
	print
	"""
	traceroute commands
	"""
	with open(as_list) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			num=ll[2:]
			if not num in mapping_dict:
				print num+' not in caida'
				continue
			AS_16bit='AS'+mapping_dict[num]
			for prefix in prefix_set:
				prefix = prefix+'/32'
				com = 'bgp router '+AS_16bit+' record-route '+prefix
				# print com
				fo.write(com+'\n') 		


