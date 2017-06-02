import networkx as nx
import matplotlib.pyplot as plt
import itertools
import sys

from pylab import rcParams
rcParams['figure.figsize'] = 44,33

if len(sys.argv) < 4:
	print "usage gephidraw.py <COUNTRY_CODE> <MODE> <U/D> <S/N>"
	print "MODE:"
	print "   1: country all to all"
	print "   2: country to imp"
	print "U<Undirected>/D<Directed>"
	print "<S/N> using start/ not using start"
	exit()
COUNTRY_CODE = sys.argv[1]
MODE = sys.argv[2]
STRUCTURE = sys.argv[3]
#path file
if MODE == "1":
	PATH_SUFFIX = "_country_all"
elif MODE == "2":
	PATH_SUFFIX = "_imp"
PATH_FILE="./"+COUNTRY_CODE+"_gao_cbgp_paths" + PATH_SUFFIX + ".txt"

"""Constants"""
IS_CBGP=False

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
				ll = line.strip()
				splits = ll.split(' ')
				if not splits[2] in dest_as_list:
					dest_as_list.append(splits[2])
print "dest_as_list " + str(dest_as_list) 

G=nx.DiGraph()
if STRUCTURE == "D":
	if len(sys.argv) < 5:
		print "<S/N> using start/ not using start"
	if sys.argv[4] == "S":
		USING_START = True
		print "USING_START " + str(USING_START)
	else:
		USING_START = False
		print "USING_START " + str(USING_START)	
	if USING_START:
		START = "start"
		G.add_node(START)

with open(PATH_FILE) as fi:
	count=0
	for line in fi:
		ll=line.strip()
		splits=ll.split(' ')
		temp_set=set()
		if count==100000:
			print '.'
			count=0
		count=count+1
		for idx in range(len(splits)-1, 1, -1): #upto before start AS index.
			currAS=splits[idx]
			prevAS=splits[idx - 1]
			G.add_node(currAS)
			G.add_node(prevAS)
			if USING_START:
				if currAS in dest_as_list:
					pass
				else:
					G.add_edge(START, currAS)

				if prevAS in dest_as_list:
					pass
				else:
					G.add_edge(START, prevAS)

			if currAS!=prevAS: # both vertex should not be same
				if IS_CBGP:
					actualCurrentAS=mapping_dict[currAS]
					actualPrevAS=mapping_dict[prevAS]
					G.add_edge(actualCurrentAS, actualPrevAS)
					# add light grey color to edges
					G[actualCurrentAS][actualPrevAS]['viz'] = {'color': {'r': 139, 'g': 144, 'b': 153, 'a': 0}}
				else:
					G.add_edge(currAS, prevAS)
					G[currAS][prevAS]['viz'] = {'color': {'r': 139, 'g': 144, 'b': 153, 'a': 0}}



# Remove nodes with low neighbour count
# Donot remove destination nodes
all_node_list = []
for node in G.nodes():
	# WARNING: should match parameters in cut finding code.
	if len(G.neighbors(node)) < 1 and (not node in dest_as_list): 
		G.remove_node(node)
		print "removed node " + node + "\n"
	elif node in dest_as_list:
		all_node_list.append(node)
		G.node[node]['viz'] = {'color': {'r': 99, 'g': 235, 'b': 146, 'a': 0}}
	else:
		all_node_list.append(node)
		G.node[node]['viz'] = {'color': {'r': 243, 'g': 255, 'b': 158, 'a': 0}}

print "all_node_list "+str(G.nodes()) + "\n"
print "len all_node_list " + str(len(G.nodes())) + "\n"

# fig = plt.figure()
# fig.patch.set_alpha(0.0)
# pos = nx.spring_layout(G)
# ax = fig.add_subplot(111)
# ax.patch.set_alpha(0.0)
# nx.draw_networkx_nodes(G, pos=pos, 
# 						nodelist = G.nodes(),
# 						node_color='y',
# 						node_size=400,
# 						alpha=0.6)
# nx.draw_networkx_edges(G, pos=pos, edgelist = G.edges(), width = 0.5)
# nx.draw_networkx_labels(G, pos=pos, font_size=10)

"""
color nodes in cut vertex set.
"""
fi = open("temp.txt")
cut_node_list = []
for node in fi:
	node =node.strip()
	if node in all_node_list:
		cut_node_list.append(node)
		if not node in dest_as_list:
			G.node[node]['viz'] = {'color': {'r': 131, 'g': 156, 'b': 255, 'a': 0}}
	
print "cut_node_list " + str(cut_node_list) + "\n"
print "len cut_node_list " + str(len(cut_node_list)) + "\n"

for node in G.nodes():
	if not node in dest_as_list and len(G.in_edges(node)) < 2:
		all_neighbor_victims = True
		for neighbor in G.neighbors(node):
			if not neighbor in dest_as_list:
				all_neighbor_victims = False
				# print node, neighbor
				break
		if all_neighbor_victims:
			# G.node[node]['viz'] = {'color': {'r': 231, 'g': 106, 'b': 195, 'a': 0}}
			print "node"
			G.remove_node(node)
		

# nx.draw_networkx_nodes(G,pos,
#                        nodelist=cut_node_list,
#                        node_color='b',
#                        node_size=500,
#                    	   alpha=0.8)

# fig.savefig('IL_15bank.pdf', format='pdf')
# nx.write_graphml(G,'so.graphml')
OUTPUT_GEPHI_FILE = "graph_"+COUNTRY_CODE+"_directed.gexf"
print "OUTPUT_GEPHI_FILE " + OUTPUT_GEPHI_FILE
nx.write_gexf(G, OUTPUT_GEPHI_FILE, version="1.2draft")
plt.show()

