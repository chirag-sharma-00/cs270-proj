import networkx as nx
from networkx.algorithms.flow.utils import build_residual_network
from scipy.optimize import linprog

def max_flow(G: nx.DiGraph, s, t):
	ans = 0
	R = build_residual_network(G, "capacity")
	_R = build_residual_network(G, "capacity")
	dist = {}
	for u in R:
		for e in R[u].values():
			e["capacity"] = 0
			e["flow"] = 0

	def dfs(u, flow):
		if (u == t) or (flow == 0):
			return flow
		res = 0
		for v, attr in R.succ[u].items():
			if (dist[v] == dist[u] + 1) and (attr["flow"] < attr["capacity"]):
				tmp = dfs(v, min(flow, attr["capacity"] - attr["flow"]))
				res += tmp
				flow -= tmp
				R.succ[u][v]["flow"] += tmp
				R.succ[v][u]["flow"] -= tmp
				if (flow == 0):
					break
		if (res==0):
			dist[u] = -1
		return res

	def bfs():
		for u in R:
			dist[u] = -1
		dist[s] = 1
		q = [s]
		for u in q:
			for v, attr in R.succ[u].items():
				if (dist[v] == -1) and (attr["flow"] < attr["capacity"]):
					dist[v] = dist[u] + 1
					q.append(v)
					if v == t:
						return True
		return False

	w = 0
	tmp = R.graph["inf"]
	while (tmp>0):
		tmp = tmp >> 1
		w +=1

	while (w >= 0):
		for u in R:
			for v, attr in R.succ[u].items():
				R.succ[u][v]["capacity"] *= 2
				R.succ[u][v]["flow"] *= 2
				if (_R.succ[u][v]["capacity"] >> w & 1):
					R.succ[u][v]["capacity"] += 1
		ans *= 2
		w -= 1
		while bfs():
			ans += dfs(s, R.graph["inf"])

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