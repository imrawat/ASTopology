"""
"""

AS_FILE='./qi_as.txt'
FILE_NAME='./ribout.txt'

my_dict=dict()
asset=set()
with open(AS_FILE) as fa:
	for AS in fa:
		asset.add(AS.strip())

print asset
with open(FILE_NAME) as fi:
	count=0
	for line in fi:
		ll=line[:len(line)-1]
		splits=ll.split(' ')
		home = splits[1]
		if home in asset:
			print ll
			prefix=splits[0]
			key = prefix+':'+home
			if not key in my_dict:
				my_dict[key]=1
			else:
				my_dict[key]=my_dict[key]+1


for AS in asset:
	total=0
	multiple=0
	for key in my_dict:
		splits=key.split(':')
		if splits[1]==AS:
#			print key+' : '+str(my_dict[key])
			if my_dict[key]>1:
				multiple=multiple+1
			total=total+1
	print '------------------------------------------'
	print 'AS : '+AS
	print 'total='+str(total)
	print 'multiple='+str(multiple)

