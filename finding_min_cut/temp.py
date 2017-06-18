

fi = open('temp.txt')

paths_dict = dict()
path_nums_with_node_dict = dict()
heuristic_weight_dict = dict()

path_num = 0
for line in fi:
	line = line.strip()
	splits = line.split(' ')
	temp_set=set()

	if len(splits) < 2:
		continue
	path_num = path_num + 1
	paths_dict[path_num] = line
	for idx in range(len(splits) - 2, 1, -1):
		AS = splits[idx]
		if AS in path_nums_with_node_dict:
			path_nums_with_node_dict[AS].add(path_num)
		else:
			path_nums_with_node_dict[AS] = set()
			path_nums_with_node_dict[AS].add(path_num)

print 'paths_dict', paths_dict
print
print 'path_nums_with_node_dict', path_nums_with_node_dict