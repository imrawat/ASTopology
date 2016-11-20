"""
program to print all those paths that start and end with AS passed in the argument.
this program checks raw bgp routeviews data and not finalspaths.txt
"""

import sys

one = sys.argv[1]
two = sys.argv[2]

for folder in range(1,19):
	file_path = './'+str(folder)+'/RIB21.txt'
	print 'searching '+file_path

	with open(file_path) as fi:
		for line in fi:
			line=line.strip()
			ll=line
#			ll=line[:len(line)-1]
			splits=ll.split(" ")
			if len(splits)<4:
				continue;
			if (splits[1]==one and  splits[len(splits)-1]==two) or (splits[1]==two and  splits[len(splits)-1]==one):
				print ll
#			if (splits[1]==one or splits[len(splits)-1]==one):
#				print ll
