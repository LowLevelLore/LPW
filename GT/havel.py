from typing import List
import networkx as nx  # type: ignore
import matplotlib.pyplot as plt  # type: ignore


def is_graphic(seq: List[int], labels: List[int]):
    if sum(seq) == 0:
        return True

    first = seq[0]
    new_seq = seq[1:]
    new_labels = [x for _, x in sorted(zip(new_seq, labels[1:]), reverse=True)]

    if len(new_seq) < first:
        return False

    for i in range(0, first):
        if new_seq[i] == 0:
            return False
        new_seq[i] -= 1

    new_seq.sort(reverse=True)
    return is_graphic(new_seq, new_labels)


def construct_adj_matrix(seq: List[int], labels: List[int]):
    n = len(seq)
    adj_matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if seq[i] > 0 and seq[j] > 0:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
                seq[i] -= 1
                seq[j] -= 1

    return adj_matrix


def plot_graph(adj_matrix, labels):
    G = nx.Graph()
    n = len(adj_matrix)

    for i in range(n):
        G.add_node(labels[i])

    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] == 1:
                G.add_edge(labels[i], labels[j])

    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=500,
        font_size=10,
    )
    plt.show()


def main():
    degree_seq = [5, 4, 3, 3, 3, 2, 2, 0]

    if sum(degree_seq) % 2 != 0:
        print("Not GRAPHIC!!")
        return

    degree_seq.sort(reverse=True)
    labels = list("abcdefghijklmnopqrstuvwxyz")[: len(degree_seq)]

    if is_graphic(degree_seq.copy(), labels.copy()):
        print("GRAPHIC")
        adj_matrix = construct_adj_matrix(degree_seq.copy(), labels.copy())
        print("Adjacency Matrix: ")
        for row in adj_matrix:
            print(row)

        plot_graph(adj_matrix, labels)
    else:
        print("Not GRAPHIC!!")


if __name__ == "__main__":
    main()
