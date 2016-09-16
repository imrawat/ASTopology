with open("./ASList.txt") as f:
    ases = f.readlines()

with open("./finalpaths.txt") as f2:
    paths = f2.readlines()

for asstr in ases:
	asnum = asstr[2:len(asstr)-1]
	print 'path from '+asstr
	for path in paths:
		pathcopy = path
		splits = path.split(' ')
		endas = splits[len(splits)-2]
		if(endas==asnum):
			print pathcopy[0:len(pathcopy)-1]
		
	print '\n\n'
		
