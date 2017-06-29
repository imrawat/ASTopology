# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization: IIIT Delhi
# Date : 28/06/16

import sys
sys.path.append('./finding_min_cut')
import argparse
import collections
import operator
import networkx as nx
from collections import OrderedDict

#local imports
import constants
from as_graph_utility import as_digraph
from as_graph_utility import compute_degrees
from get_network_boundary import get_network_boundary_impl

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'Check ')
	parser.add_argument('-c', '--country_code', help='convert to gao', required = True)
	parser.add_argument('-m', '--mode', help='convert to gao', required = True)
	
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	MODE = args.mode

	if MODE == 'C':
		SUFFIX = "_country_all"
		SUFFIX_INCLUDING_OUTSIDE = "_country_all_including_outside"
	elif MODE == 'T':
		SUFFIX = "_imp_transport"
		SUFFIX_INCLUDING_OUTSIDE = "_imp_transport_including_outside"
	elif MODE == "B":
		SUFFIX = "_imp_bank"
		SUFFIX_INCLUDING_OUTSIDE = "_imp_bank_including_outside"
	elif MODE == "G":
		SUFFIX = "_imp_govt"
		SUFFIX_INCLUDING_OUTSIDE = "_imp_govt_including_outside"
	elif MODE == "D":
		SUFFIX = "_imp_dns"
		SUFFIX_INCLUDING_OUTSIDE = "_imp_dns_including_outside"
	elif MODE == "G2C" or MODE == "g2c":
		SUFFIX = "_g2c"
		SUFFIX_INCLUDING_OUTSIDE = "_g2c_including_outside"
	elif MODE == "A2C" or MODE == "a2c":
		SUFFIX = "_a2c"
		SUFFIX_INCLUDING_OUTSIDE = "_a2c_including_outside"

	PATH_FILE = out_file = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_gao_cbgp_paths" + SUFFIX + ".txt"
	# PATH_FILE = "temp.txt"

	(G, all_start_as, all_dest_as) = as_digraph(PATH_FILE, False, False, False, None, None, None, None)
	(customers, providers, peers, customers_count, provider_count, peers_count) = compute_degrees()
	AS_FILE = constants.TEST_DATA + COUNTRY_CODE + "/" + COUNTRY_CODE + "_AS.txt"
	network_boundary = get_network_boundary_impl(AS_FILE)
	betweenness_centrality_dict = nx.betweenness_centrality(G)
	

	pf_dict = dict()
	path_as_set = set()
	fi = open(PATH_FILE)
	for line in fi:
		line = line.strip()
		splits = line.split()
		for idx in range(len(splits) - 2, 0, -1):
			path_as_set.add(splits[idx])
			if not splits[idx] in pf_dict:
				pf_dict[splits[idx]] = 1
			else:
				pf_dict[splits[idx]] = pf_dict[splits[idx]] + 1


	ordered_pf_dict = collections.OrderedDict(sorted(pf_dict.items(), key=operator.itemgetter(1), reverse = True))
	ordered_betweenness_centrality_dict = collections.OrderedDict(sorted(betweenness_centrality_dict.items(), key=operator.itemgetter(1), reverse = True))
	

	temp_dict = dict()
	for key in customers_count:
		if key in path_as_set:
			temp_dict[key] = customers_count[key]
	ordered_customers_dict = collections.OrderedDict(sorted(temp_dict.items(), key=operator.itemgetter(1), reverse = True))	

	temp_dict = dict()
	for key in provider_count:
		if key in path_as_set:
			temp_dict[key] = provider_count[key]
	ordered_providers_dict = collections.OrderedDict(sorted(temp_dict.items(), key=operator.itemgetter(1), reverse = True))

	temp_dict = dict()
	for key in peers_count:
		
		if key in path_as_set:
			temp_dict[key] = peers_count[key]
	ordered_peers_dict = collections.OrderedDict(sorted(temp_dict.items(), key=operator.itemgetter(1), reverse = True))


	ordered_dict_dict = OrderedDict()
	ordered_dict_dict['path freq'] = ordered_pf_dict
	ordered_dict_dict['customers'] = ordered_customers_dict
	ordered_dict_dict['providers'] = ordered_providers_dict
	ordered_dict_dict['peers'] = ordered_peers_dict
	ordered_dict_dict['betweenness_centrality'] = ordered_betweenness_centrality_dict
	
	

	
	print COUNTRY_CODE
	print 'len(network_boundary)', len(network_boundary)
	pf_node_list = []
	for key in ordered_dict_dict:
		percentages = [90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0]
		ordered_dict = ordered_dict_dict[key]
		print key
		for upto in range(1, len(ordered_dict) + 1):
			if len(percentages) < 1:
				break
			node_list = list(ordered_dict)[0:upto]
			fi = open(PATH_FILE)
			total_path_count = 0.0
			covered_path_count = 0.0
			for line in fi:
				total_path_count = total_path_count + 1.0
				line = line.strip()
				splits = line.split()
				for idx in range(len(splits) - 2, 0, -1):
					if splits[idx] in node_list:
						covered_path_count = covered_path_count + 1.0
						break
			
			if ((covered_path_count / total_path_count) * 100) >= percentages[0]:
				print len(node_list), ((covered_path_count / total_path_count) * 100)
				if percentages[0] == 90.0:
					print 'diff network_boundary', len(set(node_list) - network_boundary), set(node_list) - network_boundary
					if key == 'path freq':
						pf_node_list = node_list
					if not key == 'path freq':
						print 'diff pf_list_for_90', len(set(node_list) - set(pf_node_list)), set(node_list) - set(pf_node_list)
				percentages.pop(0)
		print '*' * 50
	print '*' * 100









