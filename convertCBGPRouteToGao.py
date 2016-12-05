"""
Convert CBGP traceroute paths to GAO output 
format paths.
"""

out_file='./gao_cbgp_paths.txt'
fo=open(out_file, 'w')

with open('./cbgrecord-route.txt') as fi:
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
