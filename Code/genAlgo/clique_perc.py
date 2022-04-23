import networkx as nx
import matplotlib.pyplot as plt
import pylab
import time

sample_adj_matrix = {
    1 : [2, 3, 4],
    2 : [1, 3],
    3 : [1, 2, 4],
    4 : [1, 5, 6],
    5 : [4, 6, 7, 8],
    6 : [4, 5, 7, 8],
    7 : [5, 6, 8, 9],
    8 : [5, 6, 7],
    9 : [7]
    }

## Expected Output = [[1, 2, 3, 4],[4, 5, 6, 7, 8, 9]] <- Communities

def Clique_Percolation(adj_matrix, k):
    start = time.time()
    #create 
    G = nx.Graph(adj_matrix)
    cliques = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == k]
    
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
    connected_components = [list(c) for c in nx.connected_components(perculated_graph)]
    
    communities = []
    for c in connected_components:
        common_elements_in_cliques = []
        for c_num in c:
            clique = clique_map[c_num]
            common_elements_in_cliques += [x for x in clique if x not in common_elements_in_cliques]
        communities.append(common_elements_in_cliques)

    print('Time taken for function to run:', time.time() - start)
    return communities
    
    
print(Clique_Percolation(sample_adj_matrix, 3))

