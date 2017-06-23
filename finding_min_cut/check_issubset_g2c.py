
C2C_FILE = "/Users/Madhur/Google_Drive/Thesis_Mtech/Test_Data/IL/IL_gao_cbgp_paths_country_all.txt"
G2C_FILE = "/Users/Madhur/Google_Drive/Thesis_Mtech/Test_Data/IL/IL_gao_cbgp_paths_g2c_including_outside.txt"


# C2C_FILE = "/Users/Madhur/Google_Drive/Thesis_Mtech/Test_Data/IL/temp_in.txt"
# G2C_FILE = "/Users/Madhur/Google_Drive/Thesis_Mtech/Test_Data/IL/temp_g2c.txt"

inside_path_set = set()
inside_as_set = set()

fi = open(C2C_FILE)
for line in fi:
	line = line.strip()
	splits = line.split()
	
	path = ""
	for idx in range(len(splits) - 1, 0, -1):
		path = path + ":" + splits[idx]
		inside_as_set.add(splits[idx])
	path = path[1:]
	inside_path_set.add(path)

fi = open(G2C_FILE)
for line_num, line in enumerate(fi):
	line = line.strip()
	splits = line.split()
	sub_path_inc2c_found = False
	inside_as_found = False
	for idx in range(len(splits) - 1, 1, -1):
		if splits[idx] in inside_as_set:
			inside_as_found = True
			path = ""
			for in_idx in range(idx, 1, -1):
				if splits[in_idx] in inside_as_set: # g2c file has outside country AS also. remove them 
					path = path + ":" + splits[in_idx]
			path = path[1:]
			if path in inside_path_set:
				sub_path_inc2c_found = True	
				# print line
				# print 'found', path	
				break
	if not sub_path_inc2c_found and inside_as_found:
		print line_num, 'no subset', line
