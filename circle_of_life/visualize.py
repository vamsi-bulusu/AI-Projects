import networkx as nx
import matplotlib.pyplot as plt


def visualize(graph):
    G = nx.Graph()
    visual = []
    for i, j in graph.items():
        for node in j:
            visual.append([i, node])
    G.add_edges_from(visual)
    nx.draw_networkx(G)
    plt.show()
