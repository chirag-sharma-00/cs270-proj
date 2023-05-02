import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import graph_classes
import time
import Alg_FF, Alg_EK, Alg_Dinic, Alg_Dinic_LCT

alg_names = ["FF", "EK", "Dinic", "Dinic_LCT"]
runtimes = ["mnU", "m^2 n", "mn^2", "mn\\log n"]
Algs = [Alg_FF, Alg_EK, Alg_Dinic, Alg_Dinic_LCT]

def get_theoretical(alg_name, m, n, U):
    if alg_name == "FF":
        return m * n * U
    elif alg_name == "EK":
        return m**2 * n
    elif alg_name == "Dinic":
        return m * n**2
    elif alg_name == "Dinic_LCT":
        return m * n * np.log(n)
    else:
        raise NotImplementedError

for i, Alg in enumerate(Algs):
    complete_vals = []
    bipartite_vals = []
    barbell_vals = []
    for n in np.arange(2, 256, 2):
        U = 1
        G, s, t = graph_classes.complete_graph(n)
        m = len(G.edges)
        theoretical = get_theoretical(alg_names[i], m, n, U)
        nx.set_edge_attributes(G, 1, name="capacity")
        start = time.time_ns()
        Alg.max_flow(G, s, t)
        end = time.time_ns()
        complete_vals.append((theoretical, end - start))
        G, s, t = graph_classes.bipartite_graph(n)
        m = len(G.edges)
        theoretical = get_theoretical(alg_names[i], m, n, U)
        nx.set_edge_attributes(G, 1, name="capacity")
        start = time.time_ns()
        Alg.max_flow(G, s, t)
        end = time.time_ns()
        bipartite_vals.append((theoretical, end - start))
        if n >= 5:
            G, s, t = graph_classes.barbell_graph(n)
            m = len(G.edges)
            theoretical = get_theoretical(alg_names[i], m, n, U)
            nx.set_edge_attributes(G, 1, name="capacity")
            start = time.time_ns()
            Alg.max_flow(G, s, t)
            end = time.time_ns()
            barbell_vals.append((theoretical, end - start))
    plt.figure()
    x, y = zip(*complete_vals)
    plt.plot(x, y, "x", label="Complete graph")
    x, y = zip(*bipartite_vals)
    plt.plot(x, y, "o", label="Bipartite graph")
    x, y = zip(*barbell_vals)
    plt.plot(x, y, ".", label="Barbell graph")
    x_max = plt.xlim()
    plt.xlabel(f"${runtimes[i]}$")
    plt.ylabel("Observed runtime (ns)")
    plt.legend()
    plt.tight_layout()
    plt.semilogx()
    plt.semilogy()
    plt.savefig(f"{alg_names[i]}_unit_capacity_comparison.png", dpi=150)
    plt.close()
