from collections import Counter
import copy


def generate_prufer(
    tree: dict[int, set[int]] = {1: {2}, 2: {1, 3, 4}, 3: {2}, 4: {2, 5}, 5: {4}}
) -> list[int]:
    prufer_code = []
    while len(tree) != 2:
        for i, key in enumerate(tree):
            degree = len(tree[key])
            if degree == 1:
                adj = next(iter(tree[key]))
                prufer_code.append(adj)
                del tree[key]
                for k in tree:
                    if key in tree[k]:
                        tree[k].remove(key)
                break
    return prufer_code


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
    tree: dict[int, set[int]] = {1: {2}, 2: {1, 3, 4}, 3: {2}, 4: {2, 5}, 5: {4}}
    pc = generate_prufer(copy.deepcopy(tree))
    status = verify_prufer(copy.deepcopy(tree), pc)
    if status:
        print(pc)
    else:
        print("Verification failed!!")
