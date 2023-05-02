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
    random_0_2_vals = []
    random_0_4_vals = []
    random_0_6_vals = []
    random_0_8_vals = []
    for n in np.arange(2, 256, 2):
        U = 1
        G, s, t = graph_classes.random_graph(n, p=0.2)
        m = len(G.edges)
        theoretical = get_theoretical(alg_names[i], m, n, U)
        nx.set_edge_attributes(G, 1, name="capacity")
        start = time.time_ns()
        Alg.max_flow(G, s, t)
        end = time.time_ns()
        random_0_2_vals.append((theoretical, end - start))
        G, s, t = graph_classes.random_graph(n, p=0.4)
        m = len(G.edges)
        theoretical = get_theoretical(alg_names[i], m, n, U)
        nx.set_edge_attributes(G, 1, name="capacity")
        start = time.time_ns()
        Alg.max_flow(G, s, t)
        end = time.time_ns()
        random_0_4_vals.append((theoretical, end - start))
        G, s, t = graph_classes.random_graph(n, p=0.6)
        m = len(G.edges)
        theoretical = get_theoretical(alg_names[i], m, n, U)
        nx.set_edge_attributes(G, 1, name="capacity")
        start = time.time_ns()
        Alg.max_flow(G, s, t)
        end = time.time_ns()
        random_0_6_vals.append((theoretical, end - start))
        G, s, t = graph_classes.random_graph(n, p=0.8)
        m = len(G.edges)
        theoretical = get_theoretical(alg_names[i], m, n, U)
        nx.set_edge_attributes(G, 1, name="capacity")
        start = time.time_ns()
        Alg.max_flow(G, s, t)
        end = time.time_ns()
        random_0_8_vals.append((theoretical, end - start))
    plt.figure()
    x, y = zip(*random_0_2_vals)
    plt.plot(x, y, "x", label="Random graph, p = 0.2")
    x, y = zip(*random_0_4_vals)
    plt.plot(x, y, "o", label="Random graph, p = 0.4")
    x, y = zip(*random_0_6_vals)
    plt.plot(x, y, ".", label="Random graph, p = 0.6")
    x, y = zip(*random_0_8_vals)
    plt.plot(x, y, ".", label="Random graph, p = 0.8")
    x_max = plt.xlim()
    plt.xlabel(f"${runtimes[i]}$")
    plt.ylabel("Observed runtime (ns)")
    plt.legend()
    plt.tight_layout()
    plt.semilogx()
    plt.semilogy()
    plt.savefig(f"{alg_names[i]}_random_comparison.png", dpi=150)
    plt.close()
