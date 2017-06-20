# !/usr/bin/env python
# Name :  Madhur Rawat
# Organization : IIIT Delhi
# Date : 16/06/17

#local imports
import min_cut_constants
from as_graph_utility import is_reachable

''' Find if reachable and prints the path through which sink is reachable
'''
def print_path_if_reachable_capacity(G, source, sink):
    parent = dict()
    for v in G.nodes():
        parent[v] = -1
    if BFS_capacity(G, source, sink, parent):
        s = sink
        t = []
        t.append(s)
        while(s !=  source):
            s = parent[s]
            t.append(s)
        print 'path even after cut', list(reversed(t))
        return True
    else:
        return False
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
        return True
    else:
        return False

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

def trim_defense_cut(G, freq_of_node_in_cut, all_start_as, all_dest_as):
    print 'freq_of_node_in_cut', freq_of_node_in_cut
    new_union = set()
    H = G.copy()
    while(len(freq_of_node_in_cut) > 0):
        maxval = 0
        maxnode = ""
        for node in freq_of_node_in_cut:
            if freq_of_node_in_cut[node] > maxval:
                maxval = freq_of_node_in_cut[node]
                maxnode = node
        
        H.remove_nodes_from([maxnode])
        del freq_of_node_in_cut[maxnode]
        new_union.add(maxnode)
        reachable = False
        for i, AS in enumerate(all_start_as):
            for dest in all_dest_as:
                if not dest == AS:
                    if AS in H.nodes() and dest in H.nodes():
                        if is_reachable(H, AS, dest):
                            reachable = True
                            break
            if reachable:
                print 'Still reachable after removing ', maxnode
                break
        if not reachable:
            break

    H = G.copy()
    H.remove_nodes_from(new_union)
    for i, AS in enumerate(all_start_as):
        for dest in all_dest_as:
            if not dest == AS:
                if AS in H.nodes() and dest in H.nodes():
                    if is_reachable(H, AS, dest):
                        print 'is_reachable after removing new_union'
                        break

    return new_union