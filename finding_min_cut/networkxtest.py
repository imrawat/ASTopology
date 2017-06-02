import itertools
import sys
import networkx as nx
from networkx.algorithms.connectivity import local_node_connectivity
from collections import defaultdict
from networkx.algorithms.connectivity import minimum_st_node_cut
from networkx.algorithms.connectivity import minimum_st_edge_cut
from networkx.algorithms import approximation as approx
from networkx.algorithms.connectivity import (build_auxiliary_node_connectivity)
from networkx.algorithms.flow import build_residual_network

if __name__ == "__main__":
	G = nx.DiGraph()
	G.add_nodes_from([0, 1, 2, 3, 4, 5])
	G.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 2), (2, 1), (2, 4), (3, 2), (3, 5), (4, 3), (4, 5)])
	print minimum_st_node_cut(G, 0, 5)
	print "*************"
	# print minimum_st_edge_cut(G, 0, 5)
