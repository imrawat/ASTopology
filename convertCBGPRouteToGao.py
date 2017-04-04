"""
Convert CBGP traceroute paths to GAO output 
format paths.

CBGP format: 0.0.27.106 130.104.0.0/16 SUCCESS 7018 3303 2611 <where 7018 is start AS and 2611 
is home AS consisting of destination prefix>
GAO format: 130.104.0.0/16 2611 3303 7018
"""

import sys

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: python convertCBGPRouteToGao.py <COUNTRY_CODE> <MODE>"
		print "MODE:"
		print "1: country all to all"
		print "2: country to imp"
		exit()


	COUNTRY_CODE = sys.argv[1]
	MODE = sys.argv[2]

	if MODE == "1":
		PATH_SUFFIX = "_country_all"
	elif MODE == "2":
		PATH_SUFFIX = "_imp"

	OUT_FILE="./"+COUNTRY_CODE+"_gao_cbgp_paths" + PATH_SUFFIX + ".txt"
	IN_FILE="./"+COUNTRY_CODE+"_cbgp_trace" + PATH_SUFFIX + ".txt"
	print "OUT_FILE " + OUT_FILE
	print "IN_FILE " + IN_FILE

	fo=open(OUT_FILE, 'w')

	with open(IN_FILE) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			# print ll
			splits=ll.split('\t')
			# print splits
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
