import networkx as nx
import matplotlib.pyplot as plt
import itertools
from operator import itemgetter
from networkx.algorithms.connectivity import minimum_st_node_cut
from networkx.algorithms.connectivity import build_auxiliary_node_connectivity
from networkx.algorithms.flow import build_residual_network
from networkx.algorithms.connectivity.kcutsets import all_node_cuts

from networkx.algorithms.connectivity import minimum_st_edge_cut


G=nx.Graph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)

G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(5,1)

r = nx.node_connectivity(G)
possible_cuts = itertools.combinations(iter(G.nodes()), r)
for possible_cut in possible_cuts:
	H = G.copy()
	H.remove_nodes_from(possible_cut)
	if not nx.is_connected(H):
		print str(possible_cut)
	

# H = build_auxiliary_node_connectivity(G)
# R = build_residual_network(H, 'capacity')
# print minimum_st_node_cut(G, 1, 3, auxiliary=H, residual=R)
# print list(all_node_cuts(G))

# G = nx.grid_2d_graph(3, 3)

# degree = G.degree().items()
# X = {n for n, d in sorted(degree, key=itemgetter(1), reverse=True)[:2]}
# for x in X:
# 	print x
# print 

# cutsets = list(nx.all_node_cuts(G))
# print cutsets

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos=pos, nodelist = G.nodes())
nx.draw_networkx_edges(G, pos=pos, edgelist = G.edges())
nx.draw_networkx_labels(G, pos=pos, font_size=10)
plt.show()