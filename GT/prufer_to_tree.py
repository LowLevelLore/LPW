from collections import Counter
import copy


def generate_tree(prufer: list[int]) -> dict[int, set[int]]:
    tree = {}
    vertices = list(range(1, len(prufer) + 3))
    leaves = []
    for vertex in vertices:
        tree[vertex] = set()
    degree = [1] * (len(vertices) + 1)
    for vertex in prufer:
        degree[vertex] += 1
    for vertex in vertices:
        if degree[vertex] == 1:
            leaves.append(vertex)
    for code in prufer:
        leaf = leaves.pop(0)
        tree[code].add(leaf)
        tree[leaf].add(code)
        degree[code] -= 1
        if degree[code] == 1:
            leaves.append(code)
        leaves.sort()
    last_leaf = leaves.pop(0)
    second_last_leaf = leaves.pop(0)
    tree[last_leaf].add(second_last_leaf)
    tree[second_last_leaf].add(last_leaf)
    return tree


def verify_prufer(
    tree: dict[int, set[int]] = {1: {2}, 2: {1, 3, 4}, 3: {2}, 4: {2, 5}, 5: {4}},
    prufer_code=list[int],
) -> bool:
    if len(prufer_code) == len(tree) - 2:
        leaf_vertices = []
        degree_pairs = {}
        for k in tree:
            if len(tree[k]) == 1:
                leaf_vertices.append(k)
            else:
                degree_pairs[k] = len(tree[k])
        count = dict(Counter(prufer_code))
        for vertex in leaf_vertices:
            if vertex in prufer_code:
                return False
        for vertex in count:
            try:
                if count[vertex] != degree_pairs[vertex] - 1:
                    return False
            except KeyError:
                return False
        return True
    else:
        return False


if __name__ == "__main__":
    prufer = [2, 2, 4]
    tree = generate_tree(prufer=copy.deepcopy(prufer))
    status = verify_prufer(copy.deepcopy(tree), copy.deepcopy(prufer))
    if status:
        print(tree)
    else:
        print("Verification failed!!")
