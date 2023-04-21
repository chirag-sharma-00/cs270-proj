import networkx as nx
from networkx.algorithms.flow.utils import build_residual_network
from scipy.optimize import linprog

def max_flow(G: nx.DiGraph, s, t):
    ans = 0
    R = build_residual_network(G, "capacity")
    for u in R:
        for e in R[u].values():
            e["flow"] = 0

    return ans, R


if __name__=="__main__":
    G = nx.DiGraph()
    G.add_edge(1, 2, capacity=5)
    G.add_edge(1, 3, capacity=6)
    G.add_edge(1, 4, capacity=5)
    G.add_edge(2, 3, capacity=2)
    G.add_edge(2, 5, capacity=3)
    G.add_edge(3, 2, capacity=2)
    G.add_edge(3, 4, capacity=3)
    G.add_edge(3, 5, capacity=3)
    G.add_edge(3, 6, capacity=7)
    G.add_edge(4, 6, capacity=5)
    G.add_edge(5, 6, capacity=1)
    G.add_edge(6, 5, capacity=1)
    G.add_edge(5, 7, capacity=8)
    G.add_edge(6, 7, capacity=7)
    ans, R = max_flow(G, 1, 7)
    print(ans)
    # correct answer: 14
    for u, v in R.edges:
        print(u, v, R.get_edge_data(u, v))