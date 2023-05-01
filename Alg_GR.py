import networkx as nx
import math
from networkx.algorithms.flow.utils import build_residual_network
from Alg_Dinic import max_flow as blocking_flow
import copy

def max_flow(G: nx.DiGraph, s, t):
    ans = 0
    R = build_residual_network(G, "capacity")
    for u in R:
        for e in R[u].values():
            e["flow"] = 0
    n = len(G.nodes)
    m = len(G.edges)
    Lambda = math.ceil(min([math.sqrt(m), n**(2/3)]))
    #max capacity
    U = max(nx.get_edge_attributes(G, "capacity").values())
    F = m * U

    while F >= 1:
        Delta = math.ceil(F / Lambda)
        for _ in range(8 * Delta):
            l = {}
            for (u, v, attr) in R.edges(data=True):
                #residual capacity
                u_f = res_capacity(R, u, v)
                if u_f < Delta:
                    l[(u, v)] = 1
                else:
                    l[(u, v)] = 0
            d = nx.shortest_path_length(R, target=t, weight=lambda u, v, attr: l[(u, v)])
            def is_admissible(u, v):
                return d[u] == d[v] + l[(u, v)]
            #network of admissible arcs
            A = copy.deepcopy(R)
            for e in A.edges:
                if is_admissible(*e):
                    A.add_edge(e[0], e[1], capacity=res_capacity(R, e[0], e[1]))
            scc = nx.strongly_connected_components(A)
            contracted_graph = nx.condensation(A, scc=scc)
            for scc, scc_attr in contracted_graph.nodes(data=True):
                if s in scc_attr["members"]:
                    start_scc = scc
                if t in scc_attr["members"]:
                    end_scc = scc
            blocking_flow(contracted_graph, start_scc, end_scc)

def res_capacity(R: nx.DiGraph, u, v):
    return R[u][v]["capacity"] - R[u][v]["flow"] + R[v][u]["flow"]

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