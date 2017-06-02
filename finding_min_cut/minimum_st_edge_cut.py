# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization : IIIT Delhi
# Date : 16/06/17

import networkx as nx
from collections import defaultdict 

# Local imports
import min_cut_constants
from as_graph_utility import auxiliary_graph
from min_cut_utility import BFS
from min_cut_utility import BFS_capacity
from min_cut_utility import initVisited

'''
DFS on edges with valid weight
'''
def DFS(G, s, visited):
    visited[s] = True
    for v in G.neighbors(s):
        if G.edge[s][v][min_cut_constants.HEURISTIC_WEIGHT] > 0  and visited[v] == False:
            DFS(G, v, visited)

'''
DFS on edges with valid capacity
'''
def DFS_capacity(G, s, visited):
    visited[s] = True
    for v in G.neighbors(s):
        if G.edge[s][v]['capacity'] > 0  and visited[v] == False:
            DFS_capacity(G, v, visited)


def min_st_edge_cut_capacity(G, source, sink):
    # Residual Graph. G is original graph
    R = G.copy()
    parent = dict()
    for v in G.nodes():
        parent[v] = -1
    max_flow = 0 
    
    while BFS_capacity(R, source, sink, parent) :
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
    DFS_capacity(R, source, visited)
    
    single_st_edge_cut = []
    for i in R.nodes():
        for j in R.neighbors(i):
            if visited[i] and not visited[j] and G[i][j]['capacity'] > 0:
                single_st_edge_cut.append((i, j))

    return R, single_st_edge_cut


'''
Minimum st edge cut and returns residual graph
'''
def min_st_edge_cut(G, source, sink):
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
            path_flow = min (path_flow, R.edge[parent[s]][s][min_cut_constants.HEURISTIC_WEIGHT])
            s = parent[s]

        max_flow +=  path_flow

        v = sink
        while(v !=  source):
            u = parent[v]
            R.edge[u][v][min_cut_constants.HEURISTIC_WEIGHT] = R.edge[u][v][min_cut_constants.HEURISTIC_WEIGHT] - path_flow
            if not R.has_edge(v, u):
                R.add_edge(v, u)
                R.edge[v][u][min_cut_constants.HEURISTIC_WEIGHT] = 0
            R.edge[v][u][min_cut_constants.HEURISTIC_WEIGHT] = R.edge[v][u][min_cut_constants.HEURISTIC_WEIGHT] + path_flow
            v = parent[v]

    # Find nodes which can be visited
    visited = initVisited(G)
    DFS(R, source, visited)
    single_st_edge_cut = []
    for i in G.nodes():
        for j in G.neighbors(i):
            if visited[i] and not visited[j] and G.edge[i][j][min_cut_constants.HEURISTIC_WEIGHT] > 0:
                single_st_edge_cut.append((i, j))

    return R, single_st_edge_cut

# Test code
if __name__ == "__main__":
    source = 0; sink = 5

    G = nx.DiGraph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 2), (2, 1), (2, 4), (3, 2), (3, 5), (4, 3), (4, 5)])
    G.node[1][min_cut_constants.HEURISTIC_WEIGHT] = 2
    G.node[2][min_cut_constants.HEURISTIC_WEIGHT] = 3
    G.node[3][min_cut_constants.HEURISTIC_WEIGHT] = 4
    G.node[4][min_cut_constants.HEURISTIC_WEIGHT] = 5
    G.node[0][min_cut_constants.HEURISTIC_WEIGHT] = 2
    G.node[5][min_cut_constants.HEURISTIC_WEIGHT] = 4

    
    A = auxiliary_graph(G)

    R, st_cut = min_st_edge_cut(A, '%sB' % source, '%sA' % sink)
    print '*'*50
    
    for (s, t) in st_cut:
        print s, t