"""
Prepare Caida relation file for input to CBGP
-1 customer provider relation is changed to 1
| separator is changed to <SPACE>
"""
fo = open('caidarel.txt', 'w')

with open("rawcaidarel.txt") as fi:
	for line in fi:
		ll = line.strip()
		splits = ll.split('|')
		if splits[2]=='0':
			linetowrite = splits[0]+' '+splits[1]+' '+'0'+'\n'
		elif splits[2]=='-1':
			linetowrite = splits[0]+' '+splits[1]+' '+'1'+'\n'
		fo.write(linetowrite)
fo.close()
