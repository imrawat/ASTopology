# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization : IIIT Delhi
# Date : 16/06/17

#local imports
import min_cut_constants

''' Find if reachable and prints the path through which sink is reachable
'''
def print_path_if_reachable(G, source, sink):
    parent = dict()
    for v in G.nodes():
        parent[v] = -1

    if BFS(G, source, sink, parent):
        s = sink
        t = []
        t.append(s)
        while(s !=  source):
            s = parent[s]
            t.append(s)
        print 'path even after cut', list(reversed(t))

''' Similar to print_path_if_reachable this checks if sink is reachable and stores path in parent
'''
def BFS(G, s, t, parent):
    visited = initVisited(G)
    queue=[]
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.pop(0)
        for v in G.neighbors(u):

            if visited[v] == False and G.edge[u][v][min_cut_constants.HEURISTIC_WEIGHT] > 0 :
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return True if visited[t] else False

''' Similar to BFS this does walk over capacity attribute
'''
def BFS_capacity(G, s, t, parent):
    visited = initVisited(G)
    queue=[]
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.pop(0)
        for v in G.neighbors(u):
            
            if visited[v] == False and G.edge[u][v]['capacity'] > 0 :
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return True if visited[t] else False


''' BFS with 0 capacity/weight paths being valid
'''
def BFS_Thru_Zero(G, s, t, parent):
    visited = initVisited(G)
    queue=[]
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.pop(0)
        for v in G.neighbors(u):
            if visited[v] == False and G.edge[u][v][min_cut_constants.HEURISTIC_WEIGHT] == 0 :
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return True if visited[t] else False

def BFS_Thru_Zero_capacity(G, s, t, parent):
    visited = initVisited(G)
    queue=[]
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.pop(0)
        for v in G.neighbors(u):
            if visited[v] == False and G.edge[u][v]['capacity'] == 0 :
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return True if visited[t] else False

def initVisited(G):
    visited = dict()
    for v in G.nodes():
        visited[v] = False
    return visited