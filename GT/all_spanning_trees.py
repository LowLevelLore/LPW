from itertools import combinations
from typing import Dict, Set, List


def get_edges(graph: Dict[int, Set[int]]) -> List[tuple]:
    edges = set()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if (neighbor, node) not in edges:
                edges.add((node, neighbor))
    return list(edges)


def is_connected(graph: Dict[int, Set[int]], start: int) -> bool:
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node] - visited)
    return len(visited) == len(graph)


def generate_spanning_trees(graph: Dict[int, Set[int]]) -> List[Dict[int, Set[int]]]:
    nodes = list(graph.keys())
    edges = get_edges(graph)
    spanning_trees = []

    for edge_set in combinations(edges, len(graph) - 1):
        tree = {node: set() for node in nodes}
        for u, v in edge_set:
            tree[u].add(v)
            tree[v].add(u)

        if is_connected(tree, nodes[0]):
            spanning_trees.append(tree)

    return spanning_trees


graph = {
    1: {2, 3, 4, 5},
    2: {1, 3, 6},
    3: {1, 2, 4, 6},
    4: {1, 3, 5},
    5: {1, 4},
    6: {2, 3},
}
spanning_trees = generate_spanning_trees(graph)

for i, tree in enumerate(spanning_trees, 1):
    print(f"{i} -> {tree}")
