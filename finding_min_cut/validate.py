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
	cuts = ['60886', '21042', '61102', '57862', '378', '12400', '57731', '48851', '42925', '20598', '12491', '25003', '9116', '12849', '199391', '20645', '5486', '50463', '47956', '60636', '198484', '199270', '1680', '8551', '42976', '57259']
	fi = open(constants.TEST_DATA + "IL/IL_gao_cbgp_paths_a2c.txt")
	# fi = open(constants.TEST_DATA + "IL/IL_gao_cbgp_paths_country_all.txt")

	BIT16_TO_AS_MAPPING = constants.TEST_DATA + 'cbgp_16bit2AS_caida_map.txt'
	mapping_dict = get_mapping_dict(BIT16_TO_AS_MAPPING)

	needed = set()
	count = 0
	for line in fi:
		line = line.strip()
		splits = line.split()
		found = False
		for idx in range(len(splits) - 1, 0, -1):
			if splits[idx] in cuts:
			# if mapping_dict[splits[idx]] in cuts:
				found = True
				break


		if not found and len(splits) > 2:
			count = count + 1
			print 'path having not cut node ', line
			for idx in range(len(splits) - 1, 0, -1):
				needed.add(splits[idx])

	# print 'len nodes in path not found in cut', len(needed)
	print 'number of paths not having node from cut ', count

		