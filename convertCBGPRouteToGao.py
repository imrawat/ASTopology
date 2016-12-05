"""
Convert CBGP traceroute paths to GAO output 
format paths.

CBGP format: 0.0.27.106 130.104.0.0/16 SUCCESS 7018 3303 2611
GAO format: 130.104.0.0/16 2611 3303 7018
"""

#File having CBGP format traceroute paths
in_file='./cbgrecord-route.txt'

out_file='./gao_cbgp_paths.txt'
fo=open(out_file, 'w')

with open(in_file) as fi:
	for line in fi:
		ll=line[:len(line)-1]
		splits=ll.split('\t')
		prefix=splits[1]
		path=splits[3]
		psplits=path.split(' ')
		gaopath=''
		for idx in range(len(psplits)-1, -1, -1):
			gaopath=gaopath+psplits[idx]+' '
		gaopath=gaopath[:len(gaopath)-1]
		gaopath=prefix+' '+gaopath
		fo.write(gaopath+'\n')
fo.close()
