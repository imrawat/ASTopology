
dict1 = dict()
with open("IL_gao_cbgp_paths_50.txt") as fi:
	for line in fi:
		 line = line.strip()
		 splits = line.split()
		 key = splits[0] + ":" + splits[len(splits)-1]
		 val = ""
		 for split in splits:
		 	val = val + ":" + split
		 val = val[1:]
		 dict1[key] = val

dict2 = dict()
with open("IL_gao_cbgp_paths_country_all.txt") as fi:
	for line in fi:
		 line = line.strip()
		 splits = line.split()
		 key = splits[0] + ":" + splits[len(splits)-1]
		 val = ""
		 for split in splits:
		 	val = val + ":" + split
		 val = val[1:]
		 dict2[key] = val


print len(dict1)
print len(dict2)
print

for key in dict1:
	print key, dict1[key]
	if key in dict2:
		print key, dict2[key]
	print