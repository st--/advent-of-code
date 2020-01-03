import numpy as np

data = np.array(list(map(list, open('input.txt').read().splitlines())))                                                                                                                            

def plot(o=2):
    for i in range(o, data.shape[0]-o):
        for j in range(o, data.shape[1]-o):
            print(data[i,j], end='')
        print()

def simplify():
    simplified = False
    for i in range(2,data.shape[0]-2):
        for j in range(2,data.shape[1]-2):
            if data[i,j] == '.':
                numblocked = (np.array([data[i+1,j], data[i-1,j], data[i,j+1], data[i,j-1]]) == '#').sum()
                if numblocked == 3:
                    data[i,j] = '#'
                    simplified = True
    return simplified

def simplify_loop():
    while simplify():
        pass

class Graph:
    def __init__(self, symmetric=True):
        self.nodes = set()
        self.edges = {}
        self.symmetric = symmetric

    def add_edge(self, source, target, length=1):
        self.nodes.add(source)
        self.nodes.add(target)
        self.edges[source, target] = length
        if self.symmetric:
            self.edges[target, source] = length

    def neighbours(self, u):
        return [target for (source, target) in self.edges if source == u]

    def length(self, u, v):
        return self.edges[u, v]

def get_graph():
    g = Graph()
    teleports = []
    for i in range(2,data.shape[0]-2):
        for j in range(2,data.shape[1]-2):
            cur = (i,j)
            if data[cur] == '.':
                for d in 'udlr':
                    if d == 'u': nxt, oxt = (i-1,j), (i-2,j)
                    elif d == 'd': nxt, oxt = (i+1,j), (i+2,j)
                    elif d == 'l': nxt, oxt = (i,j-1), (i,j-2)
                    elif d == 'r': nxt, oxt = (i,j+1), (i,j+2)
                    if data[nxt] == '.':
                        g.add_edge(cur, nxt)
                    elif data[nxt].isalpha():
                        if d in 'dr': key = data[nxt]+data[oxt]
                        elif d in 'ul': key = data[oxt]+data[nxt]
                        else: assert False
                        if key in teleports:
                            oldkey, key = key, key + '2'
                            g.add_edge(key, oldkey, length=-1)
                        g.add_edge(cur, key)
                        teleports.append(key)
    return g

def dict_argmin(dct):
    # u = vertex in Q with min dist[u]
    min_val = np.inf
    min_key = None
    for key, val in dct.items():
        if val < min_val:
            min_val = val
            min_key = key
    return min_key

def dijkstra(graph, source, target):
    Q = []
    dist = {}
    prev = {}
    for v in graph.nodes:
        dist[v] = np.inf
        prev[v] = None
        Q.append(v)
    dist[source] = 0

    while Q:
        u = dict_argmin({u: dist[u] for u in Q})
        Q.remove(u)
        for v in graph.neighbours(u):
            # only v that are still in Q
            alt = dist[u] + graph.length(u, v)
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    return dist, prev
