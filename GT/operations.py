from typing import List, Tuple, Set, Self, Dict


class Graph:
    def __init__(self, edges: List[Tuple[str, int, int]] | None = None):
        self.__vertices: Set[int] = set()
        self.__edges: List[Tuple[str, int, int]] = []
        if edges:
            self.__edges.extend(edges)
            self.__vertices.update(
                [edge[1] for edge in edges] + [edge[2] for edge in edges]
            )

    def union(self, other: Self, mapping: Dict[str, str] | None = None) -> Self:
        new_graph = Graph()
        new_graph.__vertices.update(
            [vertex for vertex in self.__vertices]
            + [vertex for vertex in other.__vertices]
        )
        new_graph.__edges.extend(self.__edges)
        if mapping:
            new_graph.__edges.extend(list(map(lambda x: mapping[x], other.__edges)))
        else:
            new_graph.__edges.extend(other.__edges)
        new_graph.__edges = list(set(new_graph.__edges))
        return new_graph

    def intersection(self, other: Self, mapping: Dict[str, str] | None = None) -> Self:
        new_graph = Graph()
        new_graph.__vertices.update(
            [vertex for vertex in self.__vertices if vertex in other.__vertices]
        )
        new_graph.__edges = []
        for edge in other.__edges:
            edge_to_compare = edge
            if mapping:
                edge_to_compare = (mapping[edge[0]], edge[1], edge[2])
            if edge_to_compare in self.__edges:
                new_graph.__edges.append(edge)
        return new_graph

    def difference(
        self,
        other: Self,
        mapping: Dict[str, str] | None = None,
        remove_vertices: bool = True,
    ) -> Self:
        new_graph = Graph()
        if remove_vertices:
            new_graph.__vertices.update(
                [vertex for vertex in self.__vertices if vertex not in other.__vertices]
            )
        else:
            new_graph.__vertices = self.__vertices
        new_graph.__edges = []
        for edge in self.__edges:
            edge_to_compare = edge
            if mapping:
                edge_to_compare = (mapping[edge[0]], edge[1], edge[2])
            if (
                edge_to_compare not in other.__edges
                and edge_to_compare[1] in new_graph.__vertices
                and edge_to_compare[2] in new_graph.__vertices
            ):
                new_graph.__edges.append(edge)
        return new_graph

    def complement(self):
        new_graph = Graph()
        new_graph.__vertices.update(self.__vertices)
        new_graph.__edges = []
        all_possible_edges = []
        vertices = list(self.__vertices)
        for i in range(len(vertices)):
            for j in range(i, len(vertices)):
                all_possible_edges.append((i + 1, j + 1))
        naming = 1
        self_edges = list(map(lambda x: (x[1], x[2]), self.__edges))
        for edge in all_possible_edges:
            if edge not in self_edges:
                new_graph.__edges.append(("e" + str(naming), *edge))
        return new_graph

    def ring_sum(self, other: Self, mapping: Dict[str, str] | None = None) -> Self:
        intersection = self.intersection(other, mapping)
        union = self.union(other, mapping)
        return union.difference(intersection, mapping, remove_vertices=False)

    def __str__(self):
        representation = f"Graph(\n\tVertices: {self.__vertices} \n\tEdges: \n\t\t"
        for edge in self.__edges:
            representation += f"({edge[0]}, {edge[1]}, {edge[2]})"
            representation += "\n\t\t"
        representation += "\n)"
        return representation

    def print(self):
        print(self.__str__())


G1 = Graph(
    [("a", 1, 2), ("b", 1, 3), ("c", 2, 3), ("d", 2, 4), ("e", 3, 5), ("f", 4, 5)]
)
G2 = Graph(
    [("a", 1, 2), ("c", 2, 3), ("g", 1, 3), ("h", 1, 6), ("k", 3, 6), ("l", 6, 5)]
)

union = G1.union(G2)
intersection = G1.intersection(G2)
difference = G1.difference(G2)
ring_sum = G1.ring_sum(G2)
print(union)
print(intersection)
print(difference)
print(ring_sum)

G = Graph(edges=[("e1", 1, 2), ("e2", 2, 3), ("e3", 1, 4)])
G_prime = G.complement()
G_prime.print()
