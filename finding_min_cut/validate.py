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
	cuts = ['37031', '20928', '24835', '24863', '8452', '36992']
	fi = open(constants.TEST_DATA + "EG/EG_gao_cbgp_paths_country_all.txt")

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

		