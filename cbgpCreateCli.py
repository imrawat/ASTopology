"""
cbgpCreateCli.py
Create a .cli file for C-BGP which will load prefixes to AS and 
use traceroute to get path from AS to a particular prefix.
Uses alias as 16bit AS numbers
"""
import sys

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: python cbgpCreateCli.py <COUNTRY_CODE>"
		exit()

	COUNTRY_CODE = sys.argv[1]

	#File containing the AS number and its corresponding prefix to be added. This prefix will be the same which will be tracerouted.
	prefix_file='./'+COUNTRY_CODE+'_ASPrefixes.txt'

	#File containing the ASes from which traceroute will be done to prefixes
	as_list = './'+COUNTRY_CODE+'_AS.txt'

	#16bit mapped AS list
	CAIDA_REL_16BIT='./caida_16bit.txt'

	#AS to its 16bit alias mapping.
	AS_TO_16BIT_MAPPING='./cbgp_AS216bit_caida_map.txt'


	# cli file which will add prefixes to AS routers of the country 
	out_file='./'+COUNTRY_CODE+'_country_50.cli'

	fo = open(out_file, 'w')

	print 'prefix_file : '+prefix_file
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
	"""
	mapping_dict=dict()
	with open(AS_TO_16BIT_MAPPING) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			splits=ll.split(' ')
			if not splits[0] in mapping_dict:
				mapping_dict[splits[0]]=splits[1]


	"""
	add prefixes to CBGP routers. Router numbers are mapping of 
	actual AS numbers to 16bit aliases.
	"""

	count=1
	with open(prefix_file) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			splits=ll.split(' ')
			AS = splits[0]
			num=AS[2:]
			prefix = splits[1]

			if not num in mapping_dict:
				print num+' not in caida'
				continue

			if not prefix in prefix_set:
				prefix_set.add(prefix)

			# add to mapped 16bit AS instead of actual AS numbers
			AS_16bit='AS'+mapping_dict[num]
			com = 'bgp router '+AS_16bit+' add network '+prefix
			print com
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
				com = 'bgp router '+AS_16bit+' record-route '+prefix
				print com
				fo.write(com+'\n') 		


