import matplotlib.pyplot as plt
import itertools
import sys
import math
import argparse
import min_cut_constants
import networkx as nx
from networkx.algorithms.connectivity import local_node_connectivity
from collections import defaultdict
from networkx.algorithms.connectivity import minimum_st_node_cut
from networkx.algorithms import approximation as approx
from networkx.algorithms.connectivity import (build_auxiliary_node_connectivity)
from networkx.algorithms.flow import build_residual_network

# Local imports
from as_graph_utility import as_digraph
from as_graph_utility import is_reachable
from as_graph_utility import paths_between_st
from multiple_minimum_st_node_cut import multiple_minimum_st_node_cut


'''
"Usage: python prog.py <COUNTRY_CODE> <MODE> <S/N>"
"MODE:"
"   1: country all to all"
"   2: country to imp"
"<S/N> using start/ not using start"	
'''


class NodeCutDirected :

	def __init__(self,country_code, mode, using_start) :
		self.COUNTRY_CODE = country_code
		if mode == "1":
			self.MODE_SUFFIX = "_country_all"
		elif mode == "2":
			self.MODE_SUFFIX = "_imp"

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
		self.BIT16_TO_AS_MAPPING='./cbgp_16bit2AS_caida_map.txt'
		
		self.DOMAINS = ['bank', 'govt', 'transport']
		
		# Indicates that path were received from CBGP and therefore 16bit mapping was done possibly.
		self.IS_CBGP=True
		print "Note: IS_CBGP="+str(self.IS_CBGP);


	def node_cut_to_important(self) :
		dest_as_list = []
		for selected_domain in self.selected_domains:
			domain = self.DOMAINS[int(selected_domain) - 1]
			domain_file = './'+self.COUNTRY_CODE+'_'+domain+'.txt'

			self.add_dest_as(domain_file, dest_as_list)

			PATH_FILE="./"+self.COUNTRY_CODE+"_gao_cbgp_paths" + self.MODE_SUFFIX + "_" + self.DOMAINS[int(selected_domain) - 1] + ".txt"
			print "PATH_FILE " + PATH_FILE
			
			mapping_dict = self.get_mapping_dict(self.BIT16_TO_AS_MAPPING)
			
			G, all_as_set = as_digraph(PATH_FILE, self.IS_CBGP, self.USING_START, mapping_dict, dest_as_list)
			
			union = set()

			# Remove nodes with low neighbour count
			# Donot remove if its destination node. 
			# TODO: Check if this is required.
			for node in G.nodes():
				if not node in dest_as_list and len(G.in_edges(node)) < 2:
					all_neighbor_victims = True
					for neighbor in G.neighbors(node):
						if not neighbor in dest_as_list:
							all_neighbor_victims = False
							break
					if all_neighbor_victims:
						G.remove_node(node)
						all_as_set.remove(node)


			if self.USING_START:
				for dest in dest_as_list:
					if dest in all_as_set:
						st_cuts, single_st_cut = multiple_minimum_st_node_cut(G, START, dest)
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
				# print
				# print "len(all_as_set) " + str(len(all_as_set))
				# print "len(dest_as_list) " + str(len(dest_as_list))
				# print
				for AS in all_as_set:
					# Choose non destination as source
					if not AS in dest_as_list:
						for dest in dest_as_list:
							if dest in all_as_set:
								'''
								'''
								# AS = '3491'
								# dest = '55824'

								st_cuts, single_st_cut = multiple_minimum_st_node_cut(G, AS, dest)
								print AS, dest
								paths_between_st(G, AS, dest)
								print 'st_cuts ' + str(st_cuts)
								for st_cut in st_cuts:
									H = G.copy()
									H.remove_nodes_from(st_cut)
									print "st_cut " + str(st_cut)
									paths_between_st(H, AS, dest)
									print
								print
								# if len_st_cut <= 200:
								# 	union.update(st_cut)
								# else:
								# 	union.add(dest)
							else:
								print "warning: graph does not have node : " + dest
							raw_input("Press any key to continue...")

			print union
			print "len(union) " + str(len(union))
			print
			print "len(G.nodes()) " + str(len(G.nodes()))
			print
			raw_input("Press any key to continue...")
			print

	def node_cut_to_all(self) :
		PATH_FILE="./" + self.COUNTRY_CODE + "_gao_cbgp_paths" + self.MODE_SUFFIX + ".txt"
		print "PATH_FILE " + PATH_FILE

		mapping_dict = self.get_mapping_dict(self.BIT16_TO_AS_MAPPING)
		G, all_as_set, pf_dict = as_digraph(PATH_FILE, self.IS_CBGP, self.USING_START, mapping_dict, None)
		union = set()

		# Using Start in All to All case does not make much sense.
		if self.USING_START: 
			for dest in all_as_set:
				if dest in all_as_set:
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
			print "len(all_as_set) " + str(len(all_as_set))
			print
			count = 0

			for i, AS in enumerate(all_as_set):
				for dest in all_as_set:
					if not dest == AS:


						# AS = '5580'
						# dest = '12400'
						# AS = '5580'
						# dest = '20473'
						# AS = '12400'
						# dest = '2914'
						# AS = '12400'
						# dest = '174'
						print 'AS:', AS, ' dest:', dest

						max_pf = float('-inf')
						max_cut=()
						st_cuts, single_st_cut, max_possible_combinations = multiple_minimum_st_node_cut(G, AS, dest)
						print 'len(st_cuts)', len(st_cuts)
						print 'single_st_cut', single_st_cut
						if not max_possible_combinations == None and max_possible_combinations > min_cut_constants.MAXIMUM_POSSIBLE_COMBINATIONS_DIRECTED:
							st_cuts = []
							st_cuts.append(single_st_cut)
						elif len(st_cuts) > min_cut_constants.MAXIMUM_ALLOWED_ST_CUTS_COMBINATIONS_DIRECTED:
							st_cuts = []
							st_cuts.append(single_st_cut)

						for st_cut in st_cuts:
							H = G.copy()
							H.remove_nodes_from(st_cut)
							if not is_reachable(H, AS, dest):
								pf = 0
								for cut_node in st_cut:
									pf = pf + pf_dict[cut_node]
								# print 'st_cut', st_cut,'pf', pf
								if(pf > max_pf):
									max_pf = pf
									max_cut = st_cut
									tie=False
								elif (pf == max_pf) and pf>0:
									tie=True
						print str(i), 'max_cut', max_cut, 'max_pf', max_pf
						print
						union.update(max_cut)
					else:
						print "warning: graph does not have node : " + dest
						

		print union
		print "len(union) " + str(len(union))
		print
		print "len(G.nodes()) " + str(len(G.nodes()))
		print
		raw_input("Press any key to continue...")
		print

	def get_mapping_dict(self, BIT16_TO_AS_MAPPING) :
		"""Save 16bit to AS mapping in a dict."""
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
		print "dest_as_list " + str(dest_as_list)
		print


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'find cut for defender in directed graph')
	parser.add_argument('-c', '--country_code', help='Find Cut Directed', required = True)
	parser.add_argument('-m', '--mode', help='CENSYS Search', required = True)
	parser.add_argument('-s', '--using_start', help='CENSYS Search', required = True)
	
	args = parser.parse_args()
	COUNTRY_CODE = args.country_code
	MODE = args.mode
	using_start = args.using_start

	#Create our class object
	NC = NodeCutDirected(COUNTRY_CODE, MODE, using_start)

	if MODE == "2":
		'''
		Input from user the important locations to which to draw graph to
		'''
		print "domains " + str(NC.DOMAINS)
		print "options " + str(range(1, len(NC.DOMAINS) + 1))
		selected_imp_str = raw_input("Enter choice (space separated for multiple) ")
		selected_domains = selected_imp_str.split()
		if len(selected_domains) > len(NC.DOMAINS):
			print "length greater than domains"
			exit()
		for selected_imp in selected_domains:
			if not selected_imp.isdigit() or (int(selected_imp) - 1) > (len(NC.DOMAINS) - 1):
				print "invalid selected_imp " + selected_imp
				exit()
		NC.selected_domains = selected_domains

	# Call node cut implementation
	if MODE == "2":
		NC.node_cut_to_important()
	else:
		NC.node_cut_to_all()

	
	fo = open("temp.txt", "w")
	for cut_vertex in union:
		fo.write(cut_vertex+"\n");



	



	



