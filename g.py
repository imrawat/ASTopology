import networkx as nx
import matplotlib.pyplot as plt


G = nx.path_graph(4)
print G.number_of_nodes()
G.add_edge(5,6)
pos = nx.spring_layout(G)
graphs = list(nx.connected_component_subgraphs(G))
print graphs

nx.draw_networkx_nodes(G, pos=pos, nodelist = G.nodes())
nx.draw_networkx_edges(G, pos=pos, edgelist = G.edges())
nx.draw_networkx_labels(G, pos=pos, font_size=10)
plt.show()
