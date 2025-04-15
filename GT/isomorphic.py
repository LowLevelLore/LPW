n1 = int(input("Enter number of nodes in G1: "))
n2 = int(input("Enter number of nodes in G2: "))

g1 = {}
for node in range(n1):
    g1[str(node)] = set(input(f"Enter connections for node {node}, : ").split(" "))

g2 = {}
for node in range(n2):
    g2[str(node)] = set(input(f"Enter connections for node {node}, : ").split(" "))

# print(g1, g2, sep="\n")

### NON ISOMORPHIC
# g1 = {
#     "1": {"2", "6"},
#     "2": {"1", "3", "6"},
#     "3": {"2", "4", "5"},
#     "4": {"5", "3"},
#     "5": {"3", "4", "6"},
#     "6": {"1", "2", "5"},
# }

# g2 = {
#     "a": {"b", "f"},
#     "b": {"a", "c", "e"},
#     "c": {"b", "d", "f"},
#     "d": {"c", "e"},
#     "e": {"b", "d", "f"},
#     "f": {"a", "c", "e"},
# }

### ISOMORPHIC

# g1 = {"1": {"2", "3"}, "2": {"1", "4"}, "3": {"1", "4"}, "4": {"3", "2"}}

# g2 = {
#     "1": {"4", "3"},
#     "2": {"3", "4"},
#     "3": {"1", "2"},
#     "4": {"1", "2"},
# }

if (len(g1) != len(g2)) or (
    sum(len(x) for x in g1.values()) != sum(len(x) for x in g2.values())
):
    print("Stop joking!!")
    exit()

vertices_g2 = {}
for key in g2.keys():
    degree = len(g2[key])
    if degree not in vertices_g2:
        vertices_g2[degree] = [key]
    else:
        vertices_g2[degree].append(key)

vertices_g1 = {}
for key in g1.keys():
    degree = len(g1[key])
    if degree not in vertices_g1:
        vertices_g1[degree] = [key]
    else:
        vertices_g1[degree].append(key)


print(vertices_g1)
print(vertices_g2)


def check(mapping: dict) -> bool:
    for v1 in g1.keys():
        for neighbor in g1[v1]:
            if mapping[neighbor] not in g2[mapping[v1]]:
                return False
    return True


def helper(current_mapping: dict = {}):
    if len(current_mapping) == len(g1):
        if check(current_mapping):
            print("Graphs are isomorphic!")
            print("Mapping:", current_mapping)
            exit()
        return

    for vtx in g1.keys():
        if vtx not in current_mapping:
            for possible_vtx in vertices_g2[len(g1[vtx])]:
                if possible_vtx not in current_mapping.values():
                    current_mapping[vtx] = possible_vtx
                    helper(current_mapping)
                    del current_mapping[vtx]


helper()
print("Graphs are not isomorphic!")
