import constants

def get_mapping_dict(BIT16_TO_AS_MAPPING) :
	"""Save 16bit to AS mapping in a dict.
	"""
	mapping_dict=dict()
	with open(BIT16_TO_AS_MAPPING) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			splits=ll.split(' ')
			if not splits[0] in mapping_dict:
				mapping_dict[splits[0]]=splits[1]
	return mapping_dict

if __name__ == "__main__":
	cuts = ['56149', '23899', '45543', '56147', '131127', '24088', '45903', '131440', '38731', '131403', '38735', '131358', '131366', '45552', '59364', '131390', '55315', '56157', '55313', '45538', '7552', '18403', '7643', '131418', '131349', '131386', '38726', '131369', '55314', '24173', '45896', '38244', '24176', '23962', '45899', '7602', '131344', '55309', '201389']
	fi = open(constants.TEST_DATA + "VN/VN_gao_cbgp_paths_country_all.txt")

	BIT16_TO_AS_MAPPING = constants.TEST_DATA + 'cbgp_16bit2AS_caida_map.txt'
	mapping_dict = get_mapping_dict(BIT16_TO_AS_MAPPING)

	needed = set()
	count = 0
	for line in fi:
		line = line.strip()
		splits = line.split()
		found = False
		for idx in range(len(splits) - 1, 0, -1):
			if mapping_dict[splits[idx]] in cuts:
				found = True
				break


		if not found:# and len(splits) > 3:
			print line
			count = count + 1
			for idx in range(len(splits) - 1, 0, -1):
				needed.add(splits[idx])

	print 'nodes in path not found in cut', needed
	print 'count', count

		