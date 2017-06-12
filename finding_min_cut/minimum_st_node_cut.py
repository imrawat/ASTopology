# !/usr/bin/env python
# Name :  Madhur Rawat
# Date : 16/06/17
# Returns : Multiple S-T cut combinations. Based on zero capacity edges path of residual graph.
'''
References
----------
.. [1] Abdol-Hossein Esfahanian. Connectivity Algorithms.
http://www.cse.msu.edu/~cse835/Papers/Graph_connectivity_revised.pdf
'''
import itertools
import networkx as nx
from networkx.algorithms.connectivity import (build_auxiliary_node_connectivity)

# Local project imports
import min_cut_constants
from minimum_st_edge_cut import min_st_edge_cut
from minimum_st_edge_cut import min_st_edge_cut_capacity
from min_cut_utility import BFS_Thru_Zero_capacity
from min_cut_utility import initVisited


'''
Returns all paths with zero capacity edges namely residual paths
'''
def zero_capacity_residual_paths(G, source, sink):
	directed = G.is_directed()
	if not directed:
		print "Support only for directed graph currently"
		exit()
	paths, whole_paths, single_st_edge_cut = zero_capacity_paths_from_residual(G, source, sink)

	return paths
	
'''
Return multiple S-T node cuts
'''
def multiple_minimum_st_node_cut(G, source, sink) :
	
	directed = G.is_directed()
	if not directed:
		print "Support only for directed graph currently"
		exit()

	paths, whole_paths, single_st_edge_cut = zero_capacity_paths_from_residual(G, source, sink)
	
	# We are going to cheat here.
	# Instead of getting st node cutset using algo from auxiliary graph
	# We just select nodes along path for cutset
	product = 1
	single_st_node_cut = []
	for path in paths:
		product = product * len(path)
		if len(path) > 0:
			single_st_node_cut.append(path[len(path)-1])
	max_possible_combinations = 0
	if product > min_cut_constants.MAXIMUM_POSSIBLE_COMBINATIONS_DIRECTED:

		print 'number of combinations is very high. ', product
		print 'skipping this cut set to default st-cut' 
		max_possible_combinations = product
		return [], single_st_node_cut, max_possible_combinations

	return list(itertools.product(*paths)), single_st_node_cut, None



''' Return paths with all edges having 0 left capacity
Since weights in our graph are 1, we return complete paths along which weights are 0.
'''
def zero_capacity_paths_from_residual(G, source, sink):
	R, single_st_edge_cut = min_st_edge_cut_capacity(G, source, sink)

	parent = dict()
	for v in G.nodes():
		parent[v] = -1
	
	paths = []
	temps = []
	
	while BFS_Thru_Zero_capacity(R, source, sink, parent) :
		v = sink
		path = []
		temp = []
		temp.append(v)
		while (v != source) :
			u = parent[v]
			R[u][v]['capacity'] = 1
			v = parent[v]
			temp.append(v)
			if not v in path and v!=source:
				path.append(v)

		paths.append(path)
		temps.append(temp)
	# Whole path means path including start and end node.
	# print 'whole_residual_paths ', temps

	return paths, temps, single_st_edge_cut


if __name__ == "__main__":
	source = 0; sink = 5

	G = nx.DiGraph()
	G.add_nodes_from([0, 1, 2, 3, 4, 5])
	G.add_edge(0, 1, capacity = 1)
	G.add_edge(0, 2, capacity = 1)
	G.add_edge(1, 3, capacity = 1)
	G.add_edge(1, 2, capacity = 1)
	G.add_edge(2, 1, capacity = 1)
	G.add_edge(2, 4, capacity = 1)
	G.add_edge(3, 2, capacity = 1)
	G.add_edge(3, 5, capacity = 1)
	G.add_edge(4, 3, capacity = 1)
	G.add_edge(4, 5, capacity = 1)

# print multiple_minimum_st_node_cut(G, source, sink)