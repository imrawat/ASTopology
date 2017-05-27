# !/usr/bin/env python
# Name :  Madhur Rawat
# Date : 16/06/17

import networkx as nx

def as_digraph(path_file, IS_CBGP, USING_START, mapping_dict, dest_as_list = None) :
	
	all_as_set = set()
	G = nx.DiGraph()
	if USING_START:
		if dest_as_list == None:
			print "Warning . dest_as_list = None"
		START = "start"
		G.add_node(START)

	pf_dict = {}

	with open(path_file) as fi:
		count=0
		for line in fi:
			ll=line.strip()
			splits=ll.split(' ')
			temp_set=set()
			
			for idx in range(len(splits) - 1, 1, -1): #upto before start AS index.
				currAS = splits[idx]
				prevAS = splits[idx - 1]

				if currAS!=prevAS:	
					if IS_CBGP:
						actualCurrentAS = mapping_dict[currAS]
						actualPrevAS = mapping_dict[prevAS]
						if not actualPrevAS in pf_dict:
							pf_dict[actualPrevAS] = 1
						else:
							pf_dict[actualPrevAS] = pf_dict[actualPrevAS] + 1
						G.add_node(actualCurrentAS)
						G.add_node(actualPrevAS)
						G.add_edge(actualCurrentAS, actualPrevAS, capacity = 1)
						all_as_set.add(actualCurrentAS)
						all_as_set.add(actualPrevAS)
						if USING_START:
							if actualCurrentAS in dest_as_list:
								pass
							else:
								G.add_edge(START, actualCurrentAS, capacity = 1)

							if actualPrevAS in dest_as_list:
								pass
							else:
								G.add_edge(START, actualPrevAS, capacity = 1)
					else:
						if not prevAS in pf_dict:
							pf_dict[prevAS] = 1
						else:
							pf_dict[prevAS] = pf_dict[prevAS] + 1
						G.add_node(currAS)
						G.add_node(prevAS)
						G.add_edge(currAS, prevAS, capacity = 1)
						all_as_set.add(currAS)
						all_as_set.add(prevAS)
						if USING_START:
							if currAS in dest_as_list:
								pass
							else:
								G.add_edge(START, currAS, capacity = 1)
							if prevAS in dest_as_list:
								pass
							else:
								G.add_edge(START, prevAS, capacity = 1)

				if currAS=="SUCCESS":
					print ll
					print splits

	# for node in G.nodes():
	# 	G[node]['path_frequency'] = 0
	# for node in pf_dict:
	# 	G[node]['path_frequency'] = pf_dict[node]

	return (G, all_as_set, pf_dict)

def is_reachable(G, s, d):
		visited = dict()
		for vertex in G.nodes():
			visited[vertex] = False
		queue=[]
		queue.append(s)
		visited[s] = True
		while queue:
		    n = queue.pop(0)
		    if n == d:
		        return True
		    for i in G.neighbors(n):
		        if visited[i] == False:
		            queue.append(i)
		            visited[i] = True
		return False

def paths_between_st_util(G, u, d, visited, path):
	visited[u]= True
	path.append(u)
	print 'mhere', u
	if u ==d:
	    print list(reversed(path))
	else:
	    for i in G.neighbors(u):

	        if visited[i]==False:
	            paths_between_st_util(G, i, d, visited, path)
	path.pop()
	visited[u]= False

def paths_between_st(G ,source, sink):
	print 'paths_between_st', source, sink
	visited = dict()
	for vertex in G.nodes():
		visited[vertex] = False
	path = []
	paths_between_st_util(G, source, sink,visited, path)

if __name__ == "__main__":
	pass