import networkx
from scipy.optimize import linprog

def max_flow(G: networkx.DiGraph, source: int, sink: int, capacities: dict) -> int:
    assert source > 0 and sink > 0 and source < len(G) and sink < len(G)
    #capacities is a dict mapping edges to their capacities
    return "dict mapping each edge to value of found flow on that edge", "value of flow" 