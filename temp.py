'''
program to print all those paths that start and end with AS passed in the argument.
'''

import sys

one = sys.argv[1]
two = sys.argv[2]

with open("finalpaths.txt") as fi:
	for line in fi:
		line=line.strip()
		ll=line
#		ll=line[:len(line)-1]
		splits=ll.split(" ")
		if len(splits)<4:
			continue;
		if (splits[4]==one and  splits[len(splits)-1]==two) or (splits[4]==two and  splits[len(splits)-1]==one):
			print ll
#		if (splits[4]==one or splits[len(splits)-1]==one):
#			print ll
