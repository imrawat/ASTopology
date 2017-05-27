# !/usr/bin/env python
# Name :  Madhur Rawat
# Date : 16/06/17

def BFS(G, s, t, parent):
    visited = initVisited(G)
    queue=[]
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.pop(0)
        for v in G.neighbors(u):
            if visited[v] == False and G[u][v]['capacity'] > 0 :
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
            if visited[v] == False and G[u][v]['capacity'] == 0 :
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return True if visited[t] else False

def initVisited(G):
    visited = dict()
    for v in G.nodes():
        visited[v] = False
    return visited