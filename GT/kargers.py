import random


class UnionFind:
    def __init__(self, elements):
        self.parent = {}
        for e in elements:
            self.parent[e] = e

    def find(self, u):
        while self.parent[u] != u:
            self.parent[u] = self.parent[self.parent[u]]
            u = self.parent[u]
        return u

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            self.parent[root_v] = root_u


def kargers_min_cut(graph, edges):
    uf = UnionFind(list(graph.keys()))
    random.shuffle(edges)

    contractions_needed = len(graph) - 2
    contractions = 0
    i = 0

    while contractions < contractions_needed and i < len(edges):
        u, v = edges[i]
        i += 1
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            contractions += 1

    cutset = []
    for u, v in edges:
        if uf.find(u) != uf.find(v):
            edge = frozenset({u, v})
            cutset.append(edge)

    return frozenset(cutset)


def find_all_cutsets(graph, edges, iterations=1000):
    cutsets = set()
    min_len = float("inf")
    min_cutset = None
    for _ in range(iterations):
        cutset = kargers_min_cut(graph, edges)
        if len(cutset) > 0:
            cutsets.add(cutset)
            if len(cutset) < min_len:
                min_len = len(cutset)
                min_cutset = cutset
    return cutsets, min_cutset


if __name__ == "__main__":
    graph = {
        0: [1, 2, 3],
        1: [0, 2],
        2: [0, 1, 3],
        3: [0, 2],
    }
    edges = []
    for u in graph:
        for v in graph[u]:
            edges.append((u, v))

    cutsets, min_cutset = find_all_cutsets(graph, edges, iterations=1000)

    print(f"Found {len(cutsets)} unique cutsets.")
    for i, cutset in enumerate(cutsets):
        print(f"Cutset {i+1}: {[tuple(edge) for edge in cutset]}")

    print(f"Min Cutset: {[tuple(edge) for edge in min_cutset]}")
