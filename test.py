import os
import sys
infile='lookup.txt'
outfile='lookout.txt'
fo=open(outfile, 'w')
ft=open
with open(infile) as fi:
	for l in fi:
		line = l[:len(l)-1]
		command = 'nslookup '+line
		out = os.popen(command).read()
		fo.write(line+'\n')
		count=0
		for outline in out.splitlines():
			if(count>3):
				pref=outline[0:4]
				if(pref=='Name' or pref=='Addr'):
					fo.write(outline+'\n')
			elif(count==3):
				pref=outline[-8:]
				if(pref=='NXDOMAIN'):
					fo.write('NXDOMAIN Error'+'\n')
					break
			count=count+1
		fo.write('***********************************************************\n')