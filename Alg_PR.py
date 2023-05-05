# Implementation of Push-Relabel algorithm
# Uses relabel-to-front which should run in O(n^3) time
import networkx as nx
import pyllist
from networkx.algorithms.flow.utils import build_residual_network
from scipy.optimize import linprog

TOLERANCE = 1e-10

def max_flow(G: nx.DiGraph, s, t):
    R = build_residual_network(G, "capacity")
    # construct neighbor lists for every vertex and global vertex list
    neighbor_lists = get_neighbor_lists(R, t)
    global_list = pyllist.dllist([u for u in neighbor_lists.keys() if u != s])
    current = {u:0 for u in neighbor_lists.keys() if u != s}
    u_node = global_list.first
    h, e = init_preflow(R, s)
    while u_node is not None:
        u = u_node.value
        old_h = h[u]
        discharge(R, u, h, e, neighbor_lists, current)
        if h[u] > old_h:
            # move u to front
            global_list.remove(u_node)
            global_list.appendleft(u)
            u_node = global_list.first
        u_node = u_node.next
    
    # compute value
    ans = get_flow_value(R, t)
    return ans, R

def discharge(R: nx.digraph, u, h, e, neighbor_lists, current):
    neighbors = neighbor_lists[u]
    while e[u] > 0:
        v_index = current[u]
        if v_index >= len(neighbors):
            # relabel
            relabel(R, u, h)
            current[u] = 0
        elif get_residual_capacity(R, u, neighbors[v_index]) > TOLERANCE and h[u] == h[neighbors[v_index]] + 1:
            push(R, u, neighbors[v_index], e)
        else:
            current[u] += 1

def push(R: nx.digraph, u, v, e):
    """
    pushes flow from u to v in original graph G
    e is excess table
    """
    assert (e[u] > TOLERANCE), "u must be overflowing"

    # setup
    forward_cap = get_forward_capacity(R, u, v)
    backward_cap = get_backward_capacity(R, u, v)
    assert (forward_cap + backward_cap > TOLERANCE), "edge must have residual capacity"
    delta = min(e[u], forward_cap + backward_cap)

    # push flow
    forward = min(e[u], forward_cap)
    backward = delta - forward
    R[u][v]["flow"] += forward
    R[v][u]["flow"] -= backward

    # update excesses
    e[u] -= delta
    e[v] += delta

def relabel(R: nx.digraph, u, h):
    """
    relabels vertex u in original graph G
    """
    min_h = h[u]
    for v in R[u].keys():
        if get_residual_capacity(R, u, v) > TOLERANCE:
            min_h = min(min_h, h[v])
    h[u] = min_h + 1

def get_forward_capacity(R: nx.digraph, u, v):
    capacity = R[u][v]["capacity"]
    forward_flow = R[u][v]["flow"]
    return capacity - forward_flow

def get_backward_capacity(R: nx.digraph, u, v):
    return R[v][u]["flow"]

def get_residual_capacity(R: nx.digraph, u, v):
    return get_forward_capacity(R, u, v) + get_backward_capacity(R, u, v)

def init_preflow(R: nx.digraph, s):
    h = {} # heigh function at each vertex
    e = {} # excess flow from each vertex
    for u in R:
        h[u] = 0
        e[u] = 0
        for edge in R[u].values():
            edge["flow"] = 0
    h[s] = len(R)
    for v, edge in R[s].items():
        edge["flow"] = edge["capacity"]
        e[v] = edge["capacity"]
        e[s] -= edge["capacity"]
    return h, e

def get_neighbor_lists(R: nx.DiGraph, t):
    neighbor_lists = {}
    for u in R:
        if u != t:
            neighbor_lists[u] = list(R[u])
    return neighbor_lists

def get_flow_value(R: nx.DiGraph, t):
    value = 0
    for u in R[t].keys():
        value += R[u][t]["flow"]
    return value


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