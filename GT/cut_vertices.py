from collections import defaultdict
from typing import List, Dict


class Graph:
    def __init__(self, vertices: int, edges: Dict[int, List[int]]):
        self.V = vertices
        self.graph = defaultdict(list)
        for key in edges.keys():
            for pair in edges[key]:
                self.add_edge(key, pair)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def find_cut_vertices(self):
        def dfs(u, parent, visited, disc, low, time, ap):
            children = 0
            visited[u] = True
            disc[u] = low[u] = time[0]
            time[0] += 1

            for v in self.graph[u]:
                if not visited[v]:
                    children += 1
                    dfs(v, u, visited, disc, low, time, ap)
                    low[u] = min(low[u], low[v])

                    if parent == -1 and children > 1:
                        ap[u] = True
                    if parent != -1 and low[v] >= disc[u]:
                        ap[u] = True

                elif v != parent:
                    low[u] = min(low[u], disc[v])

        visited = [False] * self.V
        disc = [-1] * self.V
        low = [-1] * self.V
        ap = [False] * self.V
        time = [0]

        for i in range(self.V):
            if not visited[i]:
                dfs(i, -1, visited, disc, low, time, ap)

        return [i for i in range(self.V) if ap[i]]


g = Graph(5, {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2, 4], 4: [3]})

cut_vertices = g.find_cut_vertices()
print("Cut vertices:", cut_vertices)
