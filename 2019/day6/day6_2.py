import sys
sys.path.append("../day20")
from day20 import Graph, dijkstra

data = open("input.txt").read().strip().splitlines()

g = Graph()
for line in data:
    center, satellite = line.split(')')
    g.add_edge(center, satellite)

dist, prev = dijkstra(g, 'YOU', 'SAN')
print(dist['SAN'] - 2)
