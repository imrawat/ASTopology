import networkx as nx
import matplotlib.pyplot as plt
import itertools

pf_dict={}

IS_CBGP=True

#16bit AS to AS mapping
BIT16_TO_AS_MAPPING='./cbgp_16bit2AS_caida_map.txt'

"""
Save AS to 16bit mapping in a dict.
"""
mapping_dict=dict()
if IS_CBGP:
	with open(BIT16_TO_AS_MAPPING) as fi:
		for line in fi:
			ll=line[:len(line)-1]
			splits=ll.split(' ')
			if not splits[0] in mapping_dict:
				mapping_dict[splits[0]]=splits[1]

G=nx.Graph()
with open('./gao_cbgp_paths.txt') as fi:
	count=0
	for line in fi:
		ll=line[:len(line)-1]
		# print ll
		splits=ll.split(' ')
		temp_set=set()
		if count==100000:
			print '.'
			count=0
		count=count+1
		for idx in range(1, len(splits)-1): #upto before start AS index.
			currAS=splits[idx]
			nextAS=splits[idx+1]
			G.add_node(currAS)
			G.add_node(nextAS)
			if currAS!=splits[1]: #AS should not be equal to home AS in cases like '41.128.214.0/24 6127 6127 6127 6127 24863 8452'
				if not currAS in temp_set:
					temp_set.add(currAS)
			if currAS!=nextAS: # both vertex should not be same
				if IS_CBGP:
					actualCurrentAS=mapping_dict[currAS]
					actualNextAS=mapping_dict[nextAS]
					G.add_edge(actualCurrentAS, actualNextAS)
				else:
					G.add_edge(currAS, nextAS)

		#increase path freq by 1 for all non start and home AS found in above path.
		for AS in temp_set:
			if AS in pf_dict:
				pf_dict[AS]=pf_dict[AS]+1
			else:
				pf_dict[AS]=1

print pf_dict



for node in G.nodes():
	if len(G.neighbors(node))==1:
		G.remove_node(node)

# r = nx.node_connectivity(G)

# possible_cuts = itertools.combinations(iter(G.nodes()), r)

# max_pf=0
# max_cut=()
# tie=False
# for possible_cut in possible_cuts:
# 	H = G.copy()
# 	H.remove_nodes_from(possible_cut)
# 	if not nx.is_connected(H):
# 		pf=0
# 		for node in possible_cut:
# 			pf=pf_dict[node]+pf
# 		print possible_cut, pf
# 		if(pf>max_pf):
# 			max_pf=pf
# 			max_cut=possible_cut
# 			tie=False
# 		elif (pf==max_pf) and pf>0:
# 			tie=True

# print '\n'
# print max_cut, max_pf

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos=pos, nodelist = G.nodes())
nx.draw_networkx_edges(G, pos=pos, edgelist = G.edges())
nx.draw_networkx_labels(G, pos=pos, font_size=10)
plt.show()


