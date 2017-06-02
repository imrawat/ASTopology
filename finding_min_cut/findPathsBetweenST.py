import sys
import networkx as nx

def printAllPathsUtil(G, u, d, visited, path):

    visited[u]= True
    path.append(u)

    if u ==d:
        print path
    else:
        for i in G.neighbors(u):
            if visited[i]==False:
                printAllPathsUtil(G, i, d, visited, path)
                 
    path.pop()
    visited[u]= False

def printAllPaths(G ,s, d):

    visited = dict()
    for vertex in all_as_set:
    	visited[vertex] = False
    visited[START] = False
    visited[END] = False

    path = []

    printAllPathsUtil(G, s, d,visited, path)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage egcut.py <COUNTRY_CODE>"
		exit()

	#dictionary to store path frequency of ASes
	pf_dict={}

	# indicates that path were received from CBGP and therefore 16bit mapping was done possibly.
	IS_CBGP=False
	print "Note: IS_CBGP="+str(IS_CBGP);

	#16bit AS to AS mapping
	BIT16_TO_AS_MAPPING='./cbgp_16bit2AS_caida_map.txt'

	COUNTRY_CODE = sys.argv[1]

	#path file
	PATH_FILE='./'+COUNTRY_CODE+'_gao_cbgp_paths.txt'

	domains = ['bank', 'govt']
	important_prefix_files = []
	for domain in domains:
		prefix_file = './'+COUNTRY_CODE+'_'+domain+'.txt'
		important_prefix_files.append(prefix_file)

	dest_as_list = []
	for prefix_file in important_prefix_files:
		print "perfix file : "+prefix_file
		with open(prefix_file) as fi:
			for line in fi:
				ll = line.strip()
				splits = ll.split(' ')
				if not splits[2] in dest_as_list:
					dest_as_list.append(splits[2])
	print "dest_as_list " + str(dest_as_list)
	print

	"""Save 16bit to AS mapping in a dict."""
	mapping_dict=dict()
	if IS_CBGP:
		with open(BIT16_TO_AS_MAPPING) as fi:
			for line in fi:
				ll=line[:len(line)-1]
				splits=ll.split(' ')
				if not splits[0] in mapping_dict:
					mapping_dict[splits[0]]=splits[1]

	all_as_set = set()
	with open(PATH_FILE) as fi:
		for line in fi:
			ll=line.strip()
			splits=ll.split(' ')
			for idx in range(len(splits) - 1, 0, -1): #upto before start AS index.
				all_as_set.add(splits[idx])

	

	START = "start"
	END = "end"

	G = nx.DiGraph()
	G.add_node(START)
	G.add_node(END)

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

			for idx in range(len(splits) - 1, 1, -1): #upto before start AS index.

				currAS = splits[idx]
				prevAS = splits[idx - 1]

				G.add_node(currAS)
				G.add_node(prevAS)

				if currAS in dest_as_list:
					G.add_edge(currAS, END)
				else:
					G.add_edge(START, currAS)

				if prevAS in dest_as_list:
					G.add_edge(prevAS, END)
				else:
					G.add_edge(START, prevAS)

				if currAS!=prevAS:	
					if IS_CBGP:
						actualCurrentAS = mapping_dict[currAS]
						actualPrevAS = mapping_dict[prevAS]
						G.add_edge(actualCurrentAS, actualPrevAS)
					else:
						G.add_edge(currAS, prevAS)

				if currAS=="SUCCESS":
					print ll
					print splits

	# l = ['3491', '9498', '4657', '4637', '4766', '7922', '174', '20562', '5580', '4826', '4809', '15830', '3257', '1299', '9957', '2914', '30844', '37282', '209', '32614', '9116', '4755', '12849', '21320', '20473', '3356', '33802', '6774', '6453', '9885', '8551', '2516']
	l = ['24173', '45896', '45899', '3491', '7643', '55315', '131349', '45903', '7552', '55309', '18403']
	G.remove_nodes_from(l)
	printAllPaths(G, START, END)