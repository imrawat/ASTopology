"""
Create a .cli file for C-BGP which will load prefixes to AS and 
use traceroute to get path from AS to a particular prefix.
"""

COUNTRY_CODE='EG'

prefix_file='./'+COUNTRY_CODE+'_ASPrefixes.txt'
as_list = './'+COUNTRY_CODE+'_AS.txt'
AS_RELATION='./caidafin.txt'


# cli file which will add prefixes to AS routers of the country 
out_file='./'+COUNTRY_CODE+'_cli.cli'

fo = open(out_file, 'w')

print 'prefix_file : '+prefix_file
print 'out_file :'+out_file

fo.write('bgp topology load --addr-sch=local \"'+AS_RELATION+'\"\n')
fo.write('bgp topology install\n')
fo.write('bgp topology policies\n')
fo.write('bgp topology run\n')
fo.write('sim run\n')

prefix_set = set()


"""
add prefixes to CBGP routers
"""
with open(prefix_file) as fi:
	for line in fi:
		ll=line[:len(line)-1]
		# print ll
		splits=ll.split(' ')
		# print splits
		AS = splits[0]
		prefix = splits[1]
		if not prefix in prefix_set:
			prefix_set.add(prefix)
		com = 'bgp router '+AS+' add network '+prefix
		fo.write(com+'\n')
fo.write('sim run\n')

"""
traceroute commands
"""
with open(as_list) as fi:
	for line in fi:
		ll=line[:len(line)-1]
		for prefix in prefix_set:
			com = 'bgp router '+ll+' record-route '+prefix
			print com
			fo.write(com+'\n') 		


