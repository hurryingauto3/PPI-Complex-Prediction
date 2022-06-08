import networkx as nx
import time

# sample_adj_list = {
#     0: [1, 2, 3],
#     1: [0, 2],
#     2: [0, 1, 3],
#     3: [0, 4, 5],
#     4: [3, 5, 6, 7],
#     5: [3, 4, 6, 7],
#     6: [4, 5, 7, 8],
#     7: [4, 5, 6],
#     8: [6]
# }

# sample_adj_matrix = [
#     #[1, 2, 3, 4, 5, 6, 7, 8, 9]
#     [0, 2, 3, 4, 0, 0, 0, 0, 0],
#     [2, 0, 4, 0, 0, 0, 0, 0, 0],
#     [3, 4, 0, 5, 0, 0, 0, 0, 0],
#     [4, 0, 5, 0, 6, 7, 0, 0, 0],
#     [0, 0, 0, 6, 0, 8, 9, 3, 0],
#     [0, 0, 0, 7, 8, 0, 2, 4, 0],
#     [0, 0, 0, 0, 9, 2, 0, 5, 6],
#     [0, 0, 0, 0, 3, 4, 5, 0, 0],
#     [0, 0, 0, 0, 0, 0, 6, 0, 0],
# ]

# Sample Expected Output = [[0, 1, 2, 3],[3, 4, 5, 6, 7, 8]] <- Communities


def find_intensity(clique, G, k):
    prod = 1
    for i in range(len(clique)):
        for j in range(i+1, len(clique)):
            prod = prod * G[clique[i]][clique[j]]['weight']
    return prod**(2/(k*(k-1)))


def Clique_Percolation(G, k, I):
    start = time.time()
    cliques = [clique for clique in nx.enumerate_all_cliques(
        G) if (len(clique) == k and find_intensity(clique, G, k) >= I)]

    clique_map = {}
    for i in range(len(cliques)):
        clique_map[i+1] = cliques[i]
    perculated_graph = nx.Graph()
    perculated_graph.add_nodes_from(clique_map.keys())

    for i in range(len(cliques)):
        clique1 = cliques[i]
        for j in range(i, len(cliques)):
            clique2 = cliques[j]
            if len(list(set(clique1) & set(clique2))) == k-1:
                perculated_graph.add_edge(i+1, j+1)
    connected_components = [
        list(c) for c in nx.connected_components(perculated_graph)]

    communities = []
    for c in connected_components:
        common_elements_in_cliques = []
        for c_num in c:
            clique = clique_map[c_num]
            common_elements_in_cliques += [
                x for x in clique if x not in common_elements_in_cliques]
        communities.append(common_elements_in_cliques)

    print('Time taken to execute clustering via Clique Percolation:', time.time() - start)
    
    return communities


