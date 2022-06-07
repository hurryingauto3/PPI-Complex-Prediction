# from database.DatabaseOG import Database
# from cluster import Cluster
# from master import Master
# # import networkx as nx
# # import matplotlib.pyplot as plt
import numpy as np


# PPIDb = Database()
# species = 'Myxococcus xanthus'
# query = PPIDb.get_interactions_by_species(species)
# Interaction_Network = PPIDb.get_graph(query)

# clusters = Cluster(species, PPIDb)
# clusters.clusterCliquePerc()
# clusters.clusterGenAlgo()

# source == 'cliqueperc' or source == 'genalgo':

# master = Master()
# print(master.get_taxons(5))
# master.add_perc_for_specie(species)
# clusters = master.get_specie_cluster_nodes(species, 'cliqueperc')
# G = master.get_specie_cluster_graph(species, 'cliqueperc')
# nx.draw(G)
# plt.show()

# clusters = Cluster(species, PPIDb)
# clusters.clusterCliquePerc()
# print(clusters.getClusters('cliqueperc'))
# clusters.clusterGenAlgo()
# print(clusters.getClusters('genalgo'))
count = 0
for x in range(3):
    for k in range(3, 5):
        for I in np.arange(0.05, 0.6, 0.1):
            count += 1
print(count)