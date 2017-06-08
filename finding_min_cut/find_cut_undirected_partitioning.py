# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization: IIIT Delhi
# Date : 07/06/17
import math
import argparse
import networkx as nx
import itertools

#local imports
import constants
import min_cut_constants
from as_graph_utility import as_graph_undirected

""" Function to recusively find partitioning cuts in garph.
"""
def find_partitioning_cuts(G, all_partitioning_set):
	#minimum number_of_nodes required to disconnect a Graph.
	r = nx.node_connectivity(G) 
	print "node_connectivity = "+str(r)
	
	# get all combinations of size r.
	possible_cuts = itertools.combinations(iter(G.nodes()), r)
	print len(G.nodes()), r
	
	max_pf = float('-inf')
	max_cut = ()
	tie=False

	for i, possible_cut in enumerate(possible_cuts):
		print i, possible_cut
		H = G.copy()
		H.remove_nodes_from(possible_cut)
		if not nx.is_connected(H):
			pf=0
			for node in possible_cut:
				pf = G.node[node][min_cut_constants.PATH_FREQUENCY] + pf
				
			print possible_cut, pf
			if(pf>max_pf):
				max_pf=pf
				max_cut=possible_cut
				tie=False
			elif (pf==max_pf) and pf>0:
				tie=True

	print '\n'
	print max_cut, max_pf
	for m in max_cut:
		all_partitioning_set.add(m)
	print '\n'

	G.remove_nodes_from(max_cut)
	remainingGs = list(nx.connected_component_subgraphs(G))

	# Find cuts in remaining Graph partitions
	for remainingG in remainingGs:
		if remainingG.number_of_nodes() > 4:
			find_partitioning_cuts(remainingG, all_partitioning_set)
	return all_partitioning_set

def get_mapping_dict(BIT16_TO_AS_MAPPING) :
	"""Save 16bit to AS mapping in a dict."""
	mapping_dict=dict()
	
	with open(BIT16_TO_AS_MAPPING) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			splits=ll.split(' ')
			if not splits[0] in mapping_dict:
				mapping_dict[splits[0]]=splits[1]
	return mapping_dict

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'find cut by partitioning in two parts')
	parser.add_argument('-c', '--country_code', help='Find Cut', required = True)
	parser.add_argument('-b', '--base_partition_size', help='minimum number of nodes in a partition', required = False)
	
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	BASE_PARTITION_SIZE = args.base_partition_size
	if BASE_PARTITION_SIZE == None:
		BASE_PARTITION_SIZE = 3
	else:
		BASE_PARTITION_SIZE = int(BASE_PARTITION_SIZE)

	PATH_FILE = constants.TEST_DATA + COUNTRY_CODE + "_gao_cbgp_paths_country_all.txt"

	BIT16_TO_AS_MAPPING = constants.TEST_DATA + 'cbgp_16bit2AS_caida_map.txt'
	mapping_dict = get_mapping_dict(BIT16_TO_AS_MAPPING)

	G = as_graph_undirected(PATH_FILE, True, mapping_dict)
	
	print find_partitioning_cuts(G, set())

	