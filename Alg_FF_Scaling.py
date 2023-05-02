import networkx as nx
from networkx.algorithms.flow.utils import build_residual_network
from scipy.optimize import linprog

def max_flow(G: nx.DiGraph, s, t):
	ans = 0
	R = build_residual_network(G, "capacity")
	_R = build_residual_network(G, "capacity")
	path = []
	vis = {}
	for u in R:
		vis[u] = False
		for e in R[u].values():
			e["capacity"] = 0
			e["flow"] = 0

	def augment(path):
		flow = R.graph["inf"]
		it = iter(path)
		u = next(it)
		for v in it:
			attr = R.succ[u][v]
			flow = min(flow, attr["capacity"] - attr["flow"])
			u = v
		it = iter(path)
		u = next(it)
		for v in it:
			R.succ[u][v]["flow"] += flow
			R.succ[v][u]["flow"] -= flow
			u = v
		return flow

	def dfs(u):
		path.append(u)
		vis[u] = True
		if u == t:
			return True
		for v, attr in R.succ[u].items():
			if (attr["flow"] < attr["capacity"]) and (not vis[v]):
				if dfs(v):
					return True
		path.pop()
		# vis[u] = False
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
		while True:
			for u in R:
				vis[u] = False
			path = []
			if dfs(s) == True:
				ans += augment(path)
			else:
				break
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