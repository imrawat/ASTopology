import networkx as nx
import sys
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.connectivity import local_node_connectivity
from networkx.algorithms.connectivity import minimum_st_node_cut

all_cut_vertex = set()


def draw_graph_with_cuts(G):
	node_list = []
	for node in all_cut_vertex:
		node_list.append(node)

	fig = plt.figure()
	fig.patch.set_alpha(0.0)
	pos = nx.spring_layout(G)
	ax = fig.add_subplot(111)
	ax.patch.set_alpha(0.0)
	nx.draw_networkx_nodes(G, pos=pos, 
							nodelist = G.nodes(),
							node_color='y',
							node_size=400,
							alpha=0.6)
	nx.draw_networkx_edges(G, pos=pos, edgelist = G.edges())
	nx.draw_networkx_labels(G, pos=pos, font_size=10)
	nx.draw_networkx_nodes(G,pos,
	                       nodelist=node_list,
	                       node_color='b',
	                       node_size=500,
	                   	   alpha=0.8)
	plt.show()


"""
Function to recusively find cuts in garph.
"""
def find_cuts(G):
	"""
	minimum number_of_nodes required to disconnect a Graph.
	"""
	r = nx.node_connectivity(G) 
	print "node_connectivity = "+str(r)
	"""
	get all combinations of size r.
	"""
	possible_cuts = itertools.combinations(iter(G.nodes()), r)
	
	max_pf = -1
	max_cut = ()
	tie=False

	for possible_cut in possible_cuts:
		# print type(possible_cut)
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
	for m in max_cut:
		if not m in all_cut_vertex:
			all_cut_vertex.add(m)
	print '\n'
	
	"""
	Draw intermediate graphs with cut vertices observed till now
	"""
	# draw_graph_with_cuts(G_copy)

	G.remove_nodes_from(max_cut)
	remainingGs = list(nx.connected_component_subgraphs(G))

	"""
	draw Graph
	"""
	# pos = nx.spring_layout(G)
	# nx.draw_networkx_nodes(G, pos=pos, nodelist = G.nodes())
	# nx.draw_networkx_edges(G, pos=pos, edgelist = G.edges())
	# nx.draw_networkx_labels(G, pos=pos, font_size=10)
	# plt.show()

	'''
	Find cuts in remaining Graph partitions
	'''
	for remainingG in remainingGs:
		if remainingG.number_of_nodes()>4:
			find_cuts(remainingG)



if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage: python findCutGreedy.py <COUNTRY_CODE> <MODE>"
		print "MODE:"
		print "1: country all to all"
		print "2: country to imp"
		exit()

	#dictionary to store path frequency of ASes
	pf_dict={}
	indeg_dict = {}
	outdeg_dict = {}

	# indicates that path were received from CBGP and therefore 16bit mapping was done possibly.
	IS_CBGP = True
	HOMEAS_PF = False
	STARTAS_PF = True
	print "Note: IS_CBGP="+str(IS_CBGP);
	print "Considering home AS for PF " + str(HOMEAS_PF)
	print "Considering start AS for PF " + str(STARTAS_PF)

	#16bit AS to AS mapping
	BIT16_TO_AS_MAPPING='./cbgp_16bit2AS_caida_map.txt'

	COUNTRY_CODE = sys.argv[1]
	MODE = sys.argv[2]

	
	if MODE == "1":
		PATH_SUFFIX = "_country_all"
	elif MODE == "2":
		PATH_SUFFIX = "_imp"
	PATH_FILE="./"+COUNTRY_CODE+"_gao_cbgp_paths" + PATH_SUFFIX + ".txt"

	print "PATH_FILE " + PATH_FILE

	domains = ['bank', 'govt']
	important_prefix_files = []
	for domain in domains:
		prefix_file = './'+COUNTRY_CODE+'_'+domain+'.txt'
		important_prefix_files.append(prefix_file)

	dest_as_list = []
	if MODE == "2":
		for prefix_file in important_prefix_files:
			print "perfix file : "+prefix_file
			with open(prefix_file) as fi:
				for line in fi:
					if not line[0] == "#":
						ll = line.strip()
						splits = ll.split(' ')
						if not splits[2] in dest_as_list:
							dest_as_list.append(splits[2])

		print "dest_as_list " + str(dest_as_list)

	"""
	Save 16bit to AS mapping in a dict.
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
	with open(PATH_FILE) as fi:
		count=0
		for line in fi:
			ll=line.strip()
			splits=ll.split(' ')
			if len(splits) < 2:
				print "error " + ll
				continue
			temp_set=set()
			if count==100000:
				print '.'
				count=0
			count=count+1

			homeAS = splits[1]
			startAS = splits[len(splits)-1]
			if not homeAS in pf_dict:
				pf_dict[homeAS] = 0
			if not startAS in pf_dict:
				pf_dict[startAS] = 0

			for idx in range(1, len(splits) - 1): #upto before start AS index.
				currAS=splits[idx]
				nextAS=splits[idx + 1]
				
				if currAS=="SUCCESS":
					print ll
					print splits

				if currAS!=nextAS:	
					if IS_CBGP:
						actualCurrentAS = mapping_dict[currAS]
						actualNextAS = mapping_dict[nextAS]
						G.add_node(actualCurrentAS)
						G.add_node(actualNextAS)
						G.add_edge(actualCurrentAS, actualNextAS)
						if not actualNextAS in temp_set:
							temp_set.add(actualNextAS)
						if not actualCurrentAS in temp_set:
							temp_set.add(actualCurrentAS)
					else:
						G.add_node(currAS)
						G.add_node(nextAS)
						G.add_edge(currAS, nextAS)
						if not nextAS in temp_set:
							temp_set.add(nextAS)
						if not currAS in temp_set:
							temp_set.add(currAS)

			#increase path freq by 1 for all non start and home AS found in above path.
			for AS in temp_set:
				if (AS == homeAS and not HOMEAS_PF) or (AS == startAS and not STARTAS_PF):
					continue
				if AS in pf_dict:
					pf_dict[AS]=pf_dict[AS]+1
				else:
					pf_dict[AS]=1

	print
	# print pf_dict
	print



	# Remove nodes with low neighbour count
	# Donot remove if its destination node. 
	for node in G.nodes():
		if len(G.neighbors(node)) < 1 and (not node in dest_as_list):
			G.remove_node(node)

	#Save complete graph copy for plotting purposes
	G_copy = G.copy()
	# print local_node_connectivity(G, "20940", "174")
	# print minimum_st_node_cut(G, "20940", "174")
	find_cuts(G)

	fo = open("temp.txt", "w")
	for mm in all_cut_vertex:
		fo.write(mm+"\n");
	print "number of cuts " + str(len(all_cut_vertex))



