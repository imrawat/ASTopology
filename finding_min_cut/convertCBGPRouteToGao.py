"""
Convert CBGP traceroute paths to GAO output 
format paths.

CBGP format: 0.0.27.106 130.104.0.0/16 SUCCESS 7018 3303 2611 <where 7018 is start AS and 2611 is home AS consisting of destination prefix>
GAO format: 130.104.0.0/16 2611 3303 7018
"""

COUNTRY_CODE='EG'

#File having CBGP format traceroute paths
in_file='./cbgrecord-route.txt'



out_file='./'+COUNTRY_CODE+'_gao_cbgp_paths.txt'
fo=open(out_file, 'w')

with open(in_file) as fi:
	for line in fi:
		ll=line[:len(line)-1]
		print ll
		splits=ll.split('\t')
		print splits
		if splits[2]=='UNREACHABLE':
			print ll
			continue
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
