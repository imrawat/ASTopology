import networkx as nx
import matplotlib.pyplot as plt
import itertools
from random import randint

def find_cuts(G):
	"""
	minimum number_of_nodes required to disconnect a Graph.
	"""
	r = nx.node_connectivity(G) 

	"""
	get all combinations of size r.
	"""
	possible_cuts = itertools.combinations(iter(G.nodes()), r)
	
	max_pf=0
	max_cut=()
	tie=False
	for possible_cut in possible_cuts:
		H = G.copy()
		H.remove_nodes_from(possible_cut)
		if not nx.is_connected(H):
			pf=0
			for node in possible_cut:
				pf=pf_dict[node]+pf
			print possible_cut, pf
			if(pf>max_pf):
				max_pf=pf
				max_cut=possible_cut
				tie=False
			elif (pf==max_pf) and pf>0:
				tie=True

	print '\n'
	print max_cut, max_pf
	G.remove_nodes_from(max_cut)
	remainingGs = list(nx.connected_component_subgraphs(G))

	"""
	draw Graph
	"""
	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G, pos=pos, nodelist = G.nodes())
	nx.draw_networkx_edges(G, pos=pos, edgelist = G.edges())
	nx.draw_networkx_labels(G, pos=pos, font_size=10)
	plt.show()

	for remainingG in remainingGs:
		if remainingG.number_of_nodes()>2:
			find_cuts(remainingG)


pf_dict={}

"""
number of nodes we want to add to initial graph.
"""
n_nodes=30

G=nx.Graph()
for node in range(1,n_nodes+1):
	G.add_node(str(node))

"""
number of edges to add to our graph.
"""
n_edges=100

for i in range(1,100):
	"""
	get two random nodes to create an edge.
	"""
	n1=randint(1,n_nodes)
	n2=randint(1,n_nodes)
	sn1=str(n1)
	sn2=str(n2)

	"maintain a dictionary to count the path frequency of each node."
	if sn1 in pf_dict:
		pf_dict[sn1]=pf_dict[sn1]+1
	else:
		pf_dict[sn1]=1
		
	if sn2 in pf_dict:
		pf_dict[sn2]=pf_dict[sn2]+1
	else:
		pf_dict[sn2]=1
		
	G.add_edge(str(n1),str(n2))


for node in G.nodes():
	if len(G.neighbors(node))==0: #remove nodes with no connection.
		G.remove_node(node)

find_cuts(G)





