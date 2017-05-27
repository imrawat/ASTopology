# !/usr/bin/env python
# Name :  Madhur Rawat
# Date : 16/06/17
# Returns residual graph

import networkx as nx
from collections import defaultdict 

# Local imports
from min_cut_utility import BFS
from min_cut_utility import initVisited

def DFS(G, s, visited):
    visited[s] = True
    for v in G.neighbors(s):
        if G[s][v]['capacity'] > 0  and visited[v] == False:
            # DFS(G, s, visited)
            pass

def minSTEdgeCut(G, source, sink):
    # Residual Graph. G is original graph
    R = G.copy()
    parent = dict()
    for v in G.nodes():
        parent[v] = -1
    max_flow = 0 
    
    while BFS(R, source, sink, parent) :
        path_flow = float("Inf")
        s = sink
        while(s !=  source):
            path_flow = min (path_flow, R[parent[s]][s]['capacity'])
            s = parent[s]

        max_flow +=  path_flow

        v = sink
        while(v !=  source):
            u = parent[v]
            R[u][v]['capacity'] = R[u][v]['capacity'] - path_flow
            if not R.has_edge(v, u):
                R.add_edge(v, u, capacity = 0)
            R[v][u]['capacity'] = R[v][u]['capacity'] + path_flow
            v = parent[v]

    # Find nodes which can be visited
    visited = initVisited(G)
    DFS(R, source, visited)
    
    single_st_edge_cut = []
    for i in R.nodes():
        for j in R.neighbors(i):
            if visited[i] and not visited[j] and G[i][j]['capacity'] > 0:
                single_st_edge_cut.append((i, j))

    return R, single_st_edge_cut

# Test code
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

    print minSTEdgeCut(G, source, sink)