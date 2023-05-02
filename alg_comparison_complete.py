import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import graph_classes
import time
import Alg_FF, Alg_EK, Alg_Dinic, Alg_Dinic_LCT


'''comparison between algorithms on complete graphs with unit capacity'''

alg_names = ["FF", "EK", "Dinic", "Dinic_LCT"]
Algs = [Alg_FF, Alg_EK, Alg_Dinic, Alg_Dinic_LCT]

times = {a: [] for a in alg_names}

for n in np.arange(2, 256, 2):
    U = 1
    G, s, t = graph_classes.complete_graph(n)
    nx.set_edge_attributes(G, 1, name="capacity")
    for i, Alg in enumerate(Algs):
        start = time.time_ns()
        Alg.max_flow(G, s, t)
        end = time.time_ns()
        times[alg_names[i]].append(end - start)
plt.figure()
for a in alg_names:
    plt.plot(np.arange(2, 256, 2), times[a], label=a)
plt.xlabel("$n$")
plt.ylabel("Observed runtime (ns)")
plt.legend()
plt.tight_layout()
plt.semilogy()
plt.savefig("alg_comparison.png", dpi=150)
plt.close()