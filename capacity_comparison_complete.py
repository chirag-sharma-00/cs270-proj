import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import graph_classes
import time
import Alg_FF, Alg_FF_Scaling, Alg_Dinic, Alg_Dinic_Scaling


'''comparison between FF/FF_Scaling/Dinic/Dinic_Scaling on complete graphs with 
fixed n and varying capacity'''

alg_names = ["FF", "FF_Scaling", "Dinic", "Dinic_Scaling"]
Algs = [Alg_FF, Alg_FF_Scaling, Alg_Dinic, Alg_Dinic_Scaling]

times = {a: [] for a in alg_names}

for U in np.arange(2, 1024, 2):
    n = 32
    G, s, t = graph_classes.complete_graph(n)
    for u in G:
        for e in G[u].values():
            e["capacity"] = np.random.randint(1, U + 1)
    for i, Alg in enumerate(Algs):
        start = time.time_ns()
        Alg.max_flow(G, s, t)
        end = time.time_ns()
        times[alg_names[i]].append(end - start)
plt.figure()
for a in alg_names:
    plt.plot(np.arange(2, 1024, 2), times[a], label=a)
plt.xlabel("$U$")
plt.ylabel("Observed runtime (ns)")
plt.legend()
plt.tight_layout()
plt.semilogx()
plt.semilogy()
plt.savefig("capacity_comparison.png", dpi=150)
plt.close()