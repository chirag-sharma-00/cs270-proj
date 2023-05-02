import networkx as nx
from networkx.algorithms.flow.utils import build_residual_network
from scipy.optimize import linprog

# vertex index should be other than 0

def max_flow(G: nx.DiGraph, s, t):
	Null = -1
	ans = 0
	R = build_residual_network(G, "capacity")
	dist = {}
	lsn = {Null : Null}
	rsn = {Null : Null}
	val = {Null : R.graph["inf"]}
	add = {Null : 0}
	mn = {Null : R.graph["inf"]}
	argmn = {Null: 0}
	Id = {}
	fa = {Null: Null}
	for u in R:
		lsn[u] = Null
		rsn[u] = Null
		val[u] = R.graph["inf"]
		add[u] = 0
		mn[u] = R.graph["inf"]
		argmn[u] = None
		Id[u] = None
		fa[u] = Null 
		for e in R[u].values():
			e["flow"] = 0

	def Top(x):
		return (fa[x] == Null) or (lsn[fa[x]]!=x) and (rsn[fa[x]]!=x)

	def Plus(x, v):
		if (x == Null):
			return
		add[x] += v
		val[x] += v
		mn[x] += v
		if (Id[x] != None):
			a,b = Id[x]
			R.succ[a][b]["flow"] -= v
			R.succ[b][a]["flow"] += v

	def Down(x):
		if (add[x]):
			Plus(lsn[x], add[x])
			Plus(rsn[x], add[x])
			add[x] = 0

	def Up(x):
		tmp = R.graph["inf"]
		if (mn[lsn[x]] < tmp):
			tmp = mn[lsn[x]]
			argmn[x] = argmn[lsn[x]]
		if (val[x] < tmp):
			tmp = val[x]
			argmn[x] = x
		if (mn[rsn[x]] < tmp):
			tmp = mn[rsn[x]]
			argmn[x] = argmn[rsn[x]]
		mn[x] = tmp

	def Zig(x):
		y = fa[x]
		z = fa[y]
		if (y == lsn[z]):
			lsn[z] = x
		else:
			if (y == rsn[z]):
				rsn[z] = x
		fa[x] = z
		lsn[y] = rsn[x]
		if (rsn[x] != Null): fa[rsn[x]] = y
		rsn[x] = y
		fa[y] = x
		Up(y)

	def Zag(x):
		y = fa[x]
		z = fa[y]
		if (y == lsn[z]):
			lsn[z] = x
		else:
			if (y == rsn[z]):
				rsn[z] = x
		fa[x] = z
		rsn[y] = lsn[x]
		if (lsn[x] != Null): fa[lsn[x]] = y
		lsn[x] = y
		fa[y] = x
		Up(y)

	def Splay(x):
		s = []
		tmp = x
		while (not Top(tmp)):
			s.append(tmp)
			tmp = fa[tmp]
		s.append(tmp)
		s.reverse()
		for u in s:
			Down(u)
		while (not Top(x)):
			y = fa[x]
			z = fa[y]
			if (not Top(y)):
				if (x == lsn[y]):
					if (y == lsn[z]):
						Zig(y)
						Zig(x)
					else:
						Zig(x)
						Zag(x)
				else:
					if (y == lsn[z]):
						Zag(x)
						Zig(x)
					else:
						Zag(y)
						Zag(x)
			else:
				if (x == lsn[y]):
					Zig(x)
				else:
					Zag(x)
		Up(x)

	def Access(x):
		y = Null
		while (x != Null):
			Splay(x)
			rsn[x] = y
			Up(x)
			y = x
			x = fa[x]
		return y

	def Root(x):
		Access(x)
		Splay(x)
		while (lsn[x] != Null):
			x = lsn[x]
			Down(x)
		Splay(x)
		return x

	def Cut(x):
		Access(x)
		Splay(x)
		fa[lsn[x]] = Null
		lsn[x] = Null
		Up(x)

	def DeleteZero(x):
		Down(x)
		while (rsn[x]!=Null) and (mn[rsn[x]] == 0):
			x = argmn[rsn[x]]
			Splay(x)
			fa[lsn[x]] = Null
			lsn[x] = Null
			Up(x)

	def dfs(u):
		if (u == t):
			Access(s)
			Splay(t)
			tmp = mn[t]
			Plus(rsn[t], -tmp)
			DeleteZero(t)
			return tmp
		for v, attr in R.succ[u].items():
			if (dist[v] == dist[u] + 1) and (attr["flow"] < attr["capacity"]):
				Splay(u)
				fa[u] = v
				val[u] = attr["capacity"] - attr["flow"]
				Id[u] = u, v
				Up(u)
				tmp = dfs(Root(u))
				if (tmp):
					return tmp
		for v, attr in R.pred[u].items():
			if (dist[v] == dist[u] - 1):
				if (Root(v) == u): Cut(v)
		dist[u] = -1
		return 0

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

	while bfs():
		while (True):
			tmp = dfs(Root(s))
			if (not tmp):
				break
			ans += tmp
		for u in R:
			Splay(u)
			Down(u)
			lsn[u] = Null
			rsn[u] = Null
			fa[u] = Null
			add[u] = 0
			Id[u] = None
			val[u] = R.graph["inf"]
			mn[u] = R.graph["inf"]
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