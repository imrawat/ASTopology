# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization: IIIT Delhi
# Date : 15/12/16

'''
Find min node cut in graph
Either in country to country topology or in attacker to victim topology
Using either start AS or not
'''

from __future__ import division
import itertools
import sys
import math
import argparse
import networkx as nx
from networkx.algorithms.connectivity import local_node_connectivity
from collections import defaultdict
from networkx.algorithms.connectivity import minimum_st_node_cut
from networkx.algorithms import approximation as approx
from networkx.algorithms.connectivity import (build_auxiliary_node_connectivity)
from networkx.algorithms.flow import build_residual_network

# Local imports
import constants
import min_cut_constants
from min_cut_utility import BFS
from min_cut_utility import print_path_if_reachable
from min_cut_utility import trim_defense_cut
from as_graph_utility import as_digraph
from as_graph_utility import is_reachable
from as_graph_utility import paths_between_st
from as_graph_utility import auxiliary_graph
from minimum_st_node_cut import multiple_minimum_st_node_cut
from minimum_st_node_cut import zero_capacity_residual_paths
from heuristic_min_st_node_cut_impl import defense_st_cut
from heuristic_min_st_node_cut_impl import defense_cut_non_induced
from heuristic_min_st_node_cut_impl import set_heuristic_weight


'''
"Usage: python prog.py -c <COUNTRY_CODE> -m <MODE> -s <S/N>"
"MODE:"
"   1: country all to all"
"   2: country to imp"
"<S/N> using start/ not using start"	
'''


class NodeCutDirected :

	def __init__(self,country_code, mode, using_start, heuristic) :
		self.COUNTRY_CODE = country_code
		self.HEURISTIC = heuristic
		if mode == "1":
			self.MODE_SUFFIX = "_country_all"
		elif mode == "2":
			self.MODE_SUFFIX = "_imp"
		elif mode == "3":
			self.MODE_SUFFIX = "_a2c"

		if using_start == "S":
			self.USING_START = True
			print "USING_START " + str(self.USING_START)
		else:
			self.USING_START = False
			print "USING_START " + str(self.USING_START)	

		self.selected_domains = []

		'''Constants
		'''
		# 16bit AS to AS mapping
		self.BIT16_TO_AS_MAPPING = constants.TEST_DATA + 'cbgp_16bit2AS_caida_map.txt'
		
		self.DOMAINS = constants.DOMAINS
		
		# Indicates that path were received from CBGP and therefore 16bit mapping was done possibly.
		# Not required if conversion has already been done before.
		self.IS_CBGP = False
		print "Note: IS_CBGP = ", self.IS_CBGP;

	def node_cut_to_important(self) :
		START = 'start'
		union = set()
		new_union = set()

		# Every time a new domain is added we will add the paths for it to already created graph
		

		# Every time a new domain is added we need to update the pf_dict with new values for nodes.
		pf_dict = {}

		done = False
		cumulative_union = set()
		while (done == False and (not len(self.selected_domains) == self.DOMAINS)):
			'''
			Input from user the important locations to which to draw graph to
			'''
			print "domains " + str(self.DOMAINS)
			print "options " + str(range(1, len(self.DOMAINS) + 1))
			selected_imp = raw_input("Enter space separated choice. Currently single choice only. 0 to EXIT? ")
			if selected_imp == '0' or selected_imp == 0:
				done = True

				continue
			
			if not selected_imp.isdigit() or (int(selected_imp) - 1) > (len(self.DOMAINS) - 1) or selected_imp in self.selected_domains:
				print "invalid selected_imp or already selected " + selected_imp
				continue

			self.selected_domains.append(selected_imp)

			domain = self.DOMAINS[int(selected_imp) - 1]
			domain_file = constants.TEST_DATA + self.COUNTRY_CODE + "/" + self.COUNTRY_CODE + '_' + domain + '.txt'

			# donot use. use all_dest_as instead from actual paths
			dest_as_list = []
			self.add_dest_as(domain_file, dest_as_list)

			PATH_FILE = constants.TEST_DATA + self.COUNTRY_CODE + "/" + self.COUNTRY_CODE + "_gao_cbgp_paths" + self.MODE_SUFFIX + "_" + self.DOMAINS[int(selected_imp) - 1] + ".txt"
			# PATH_FILE = constants.TEST_DATA + "IL_gao_cbgp_paths_country_all.txt"
			print "PATH_FILE " + PATH_FILE
			
			mapping_dict = self.get_mapping_dict(self.BIT16_TO_AS_MAPPING)

			if self.USING_START:
				(G, all_start_as, all_dest_as) = as_digraph(PATH_FILE, self.IS_CBGP, self.USING_START, mapping_dict, dest_as_list, None, pf_dict)
				set_heuristic_weight(G, self.HEURISTIC)
				A = auxiliary_graph(G)
				for dest in all_dest_as:
					print 'START', START, 'dest', dest
					defense_cut = defense_st_cut(G, START, dest)
					print '* defense_cut', defense_cut
					print '*'*50
					union.update(defense_cut)
				

			else:
				(G, all_start_as, all_dest_as) = as_digraph(PATH_FILE, self.IS_CBGP, self.USING_START, mapping_dict, None, None, pf_dict)
				set_heuristic_weight(G, self.HEURISTIC)
				A = auxiliary_graph(G)
				
				freq_of_node_in_cut = dict()
				print
				print "len(all_start_as) " + str(len(all_start_as))
				print "len(all_dest_as) " + str(len(all_dest_as))
				print "len(G.nodes())", len(G.nodes())
				print "len(G.edges())", len(G.edges())
				print
				for i, AS in enumerate(all_start_as):
					print i, 'AS', AS
					for dest in all_dest_as:
						if not AS == dest :

							# use when all to all topology is used for all to important cutset.
							if not dest in dest_as_list:
								continue

							
							H = A.copy()
							defense_cut = defense_st_cut(H, AS, dest)
							# print '* defense_cut', defense_cut
							# print '*'*50
							union.update(defense_cut)
							
							for node in defense_cut:
								if node in freq_of_node_in_cut:
									freq_of_node_in_cut[node] = freq_of_node_in_cut[node] + 1
								else:
									freq_of_node_in_cut[node] = 1
				print 'trimming union'
				new_union = trim_defense_cut(G, freq_of_node_in_cut, all_start_as, all_dest_as)

			print 'union', union
			print "len(union) " + str(len(union))
			print
			print 'new_union', new_union
			print "len(new_union) " + str(len(new_union))
			print
			print "len(G.nodes()) " + str(len(G.nodes()))
			print
			cumulative_union.update(new_union)
			raw_input("Press any key to continue...")
			print
		print 'cumulative_union', cumulative_union
		print 'len(cumulative_union)', len(cumulative_union)

	def node_cut_non_induced_to_important(self):
		done = False
		while (done == False and (not len(self.selected_domains) == self.DOMAINS)):
			'''
			Input from user the important locations to which to draw graph to
			'''
			print "domains " + str(self.DOMAINS)
			print "options " + str(range(1, len(self.DOMAINS) + 1))
			selected_imp = raw_input("Enter space separated choice. Currently single choice only. 0 to EXIT? ")
			if selected_imp == '0' or selected_imp == 0:
				done = True
				continue
			
			if not selected_imp.isdigit() or (int(selected_imp) - 1) > (len(self.DOMAINS) - 1) or selected_imp in self.selected_domains:
				print "invalid selected_imp or already selected " + selected_imp
				continue

			self.selected_domains.append(selected_imp)

			domain = self.DOMAINS[int(selected_imp) - 1]
			domain_file = constants.TEST_DATA + self.COUNTRY_CODE + "/" + self.COUNTRY_CODE + '_' + domain + '.txt'

			# donot use. use all_dest_as instead from actual paths
			dest_as_list = []
			self.add_dest_as(domain_file, dest_as_list)

			PATH_FILE = constants.TEST_DATA + self.COUNTRY_CODE + "/" + self.COUNTRY_CODE +"_gao_cbgp_paths" + self.MODE_SUFFIX + "_" + self.DOMAINS[int(selected_imp) - 1] + ".txt"
			print "PATH_FILE " + PATH_FILE

			defense_cut_non_induced(PATH_FILE, self.HEURISTIC)


	def node_cut_non_induced_to_all(self):
		PATH_FILE = constants.TEST_DATA + self.COUNTRY_CODE + "/" + self.COUNTRY_CODE + "_gao_cbgp_paths" + self.MODE_SUFFIX + ".txt"
		print "PATH_FILE " + PATH_FILE

		mapping_dict = self.get_mapping_dict(self.BIT16_TO_AS_MAPPING)
		
		defense_cut_non_induced(PATH_FILE, self.HEURISTIC)
			

	def node_cut_to_all(self) :
		PATH_FILE = constants.TEST_DATA + self.COUNTRY_CODE + "/" + self.COUNTRY_CODE  + "_gao_cbgp_paths" + self.MODE_SUFFIX + ".txt"
		# PATH_FILE = "/Users/Madhur/Google_Drive/Thesis_Mtech/Test_Data/EG/EG2EG_finalpaths.txt"
		# PATH_FILE = "/Users/Madhur/Google_Drive/Thesis_Mtech/Test_Data/EG/EG_gao_cbgp_paths_country_56.txt"
		print "PATH_FILE " + PATH_FILE

		mapping_dict = self.get_mapping_dict(self.BIT16_TO_AS_MAPPING)
		(G, all_start_as, all_dest_as) = as_digraph(PATH_FILE, self.IS_CBGP, self.USING_START, mapping_dict, None, None, None)
		set_heuristic_weight(G, self.HEURISTIC)
		A = auxiliary_graph(G)
		union = set()
		
		print 'len(G.nodes())', len(G.nodes())
		ASFILE = constants.TEST_DATA + self.COUNTRY_CODE + "/" + self.COUNTRY_CODE  + "_AS.txt"
		fi = open(ASFILE)
		asset = set()
		print 'G.nodes()', G.nodes()
		for line in fi:
			line = line.strip()
			AS = line[2:]
			asset.add(AS)
		for node in G.nodes():
			if node not in asset:
				print '$', node

		# Using Start in All to All case does not make much sense.
		if self.USING_START: 
			for dest in all_start_as:
				if dest in all_start_as:
					print START, dest
					st_cut = minimum_st_node_cut(G, START, dest, auxiliary=H, residual=R)
					len_st_cut = len(st_cut)
					print st_cut
					print len_st_cut
					print
					if len_st_cut <= 200:
						union.update(st_cut)
					else:
						union.add(dest)
				else:
					print "warning: graph does not have node : " + dest

		else:
			print
			print "len(all_start_as) " + str(len(all_start_as))
			print "len(all_dest_as) " + str(len(all_dest_as))
			print
			count = 0
			freq_of_node_in_cut = dict()

			counter = 0
			for i, AS in enumerate(all_start_as):
				for dest in all_dest_as:
					if not dest == AS:
						
						print i, 'AS', AS, 'dest', dest
						H = A.copy()
						defense_cut = defense_st_cut(H, AS, dest)
						print '* defense_cut', defense_cut
						print '*'*50
						
						union.update(defense_cut)
						for node in defense_cut:
							if node in freq_of_node_in_cut:
								freq_of_node_in_cut[node] = freq_of_node_in_cut[node] + 1
							else:
								freq_of_node_in_cut[node] = 1
						
			new_union = trim_defense_cut(G, freq_of_node_in_cut, all_start_as, all_dest_as)

		print 'union', union
		print "len(union) " + str(len(union))
		print
		print 'new_union', new_union
		print "len(new_union) " + str(len(new_union))
		print
		print "len(G.nodes()) " + str(len(G.nodes()))
		print
		raw_input("Press any key to continue...")
		print

	def get_mapping_dict(self, BIT16_TO_AS_MAPPING) :
		"""Save 16bit to AS mapping in a dict.
		"""
		mapping_dict=dict()
		if self.IS_CBGP:
			with open(BIT16_TO_AS_MAPPING) as fi:
				for line in fi:
					ll=line[:len(line)-1]
					splits=ll.split(' ')
					if not splits[0] in mapping_dict:
						mapping_dict[splits[0]]=splits[1]
		return mapping_dict

	def add_dest_as(self, domain_file, dest_as_list) :
		with open(domain_file) as fi:
			for line in fi:
				if not line[0] == "#":
					ll = line.strip()
					splits = ll.split(' ')
					if not splits[2] in dest_as_list:
						dest_as_list.append(splits[2])
		
		print


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'find cut for defender in directed graph')
	parser.add_argument('-c', '--country_code', help='Country code for which cut is to be found', required = True)
	parser.add_argument('-m', '--mode', help='1: all to all. 2: all to imp', required = True)
	parser.add_argument('-s', '--using_start', help='S:attach attacker nodes to START N:Donot use START', required = True)
	parser.add_argument('-H', '--heuristic', help='Interger value for heuristic to use', required = False)
	parser.add_argument('-i', '--induced', help='N: Donot use induced graph approach', required = False)

	# mode: 
	# 	1: all to all
	# 	2: all non important to important
	# 	3: non induced cut


	# CUSTOMER_DEGREE = 1
	# PROVIDER_DEGREE = 2
	# PEER_DEGREE = 3
	# CUSTOMER_CONE_SIZE = 4
	# ALPHA_CENTRALITY = 5
	# BETWEENNESS_CENTRALITY = 6
	# PATH_FREQUENCY = 7
	
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	MODE = args.mode
	using_start = args.using_start
	heuristic = args.heuristic
	if not heuristic == None:
		heuristic = int(heuristic)
	induced = args.induced



	NC = NodeCutDirected(COUNTRY_CODE, MODE, using_start, heuristic)

	# Call node cut implementation
	if induced == None:
		print 'Using Induced DiGraph'
		if MODE == "2":
			NC.node_cut_to_important()
		elif MODE == "1":
			NC.node_cut_to_all()
		elif MODE == "3":
			NC.node_cut_to_all()

	elif induced == 'n' or induced == 'N':
		if MODE == "2":
			NC.node_cut_non_induced_to_important()
		elif MODE == "1":
			NC.node_cut_non_induced_to_all()





	



	



