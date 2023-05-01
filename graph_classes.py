import networkx as nx
import numpy as np
import math

#return graph, source node, sink node

def complete_graph(n):
    s, t = list(np.random.choice(n, 2, replace=False))
    return nx.complete_graph(n), s, t

def bipartite_graph(n):
    n1 = math.floor(n/2)
    n2 = n - n1
    s = np.random.randint(0, n1)
    t = np.random.randint(n1, n)
    return nx.complete_bipartite_graph(n1, n2), s, t

def barbell_graph(n):
    m1 = math.floor((n - 1)/2)
    m2 = n - 2 * m1
    s = np.random.randint(0, m1)
    t = np.random.randint(m1 + m2, n)
    return nx.barbell_graph(m1, m2), s, t

def random_graph(n, p):
    s, t = list(np.random.choice(n, 2, replace=False))
    if p < 0.3:
        return nx.fast_gnp_random_graph(n, p, directed=True), s, t
    else:
        return nx.gnp_random_graph(n, p, directed=True), s, t