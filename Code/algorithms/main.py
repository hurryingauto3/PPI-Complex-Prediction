# from database.DatabaseOG import Database
# from cluster import Cluster
# from master import Master
# # import networkx as nx
# # import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from texttable import Texttable
import latextable


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
# count = 0
# for x in range(3):
#     for k in range(3, 5):
#         for I in np.arange(0.05, 0.6, 0.1):
#             count += 1
# print(count)

data = [["Specie", "Clique Size", "Intensity", "Average Cluster Size", "Cluster Count"],
['Myxococcus xanthus', 3, 0.05, 61.25, 4],
['Myxococcus xanthus', 3, 0.15, 42.6, 5],
['Myxococcus xanthus', 3, 0.25, 24.0, 4],
['Myxococcus xanthus', 3, 0.35, 24.0, 1],
['Myxococcus xanthus', 3, 0.45, 11.0, 1],
['Myxococcus xanthus', 3, 0.55, 5.0, 1],
['Myxococcus xanthus', 4, 0.05, 48.0, 3],
['Myxococcus xanthus', 4, 0.15, 44.67, 3],
['Myxococcus xanthus', 4, 0.25, 15.0, 4],
['Myxococcus xanthus', 4, 0.35, 13.0, 1],
['Myxococcus xanthus', 4, 0.45, 5.0, 1],
['Myxococcus xanthus', 4, 0.55, 0, 0],
['Myxococcus xanthus', 5, 0.05, 38.0, 2],
['Myxococcus xanthus', 5, 0.15, 38.0, 2],
['Myxococcus xanthus', 5, 0.25, 24.0, 1],
['Myxococcus xanthus', 5, 0.35, 0, 0],
['Myxococcus xanthus', 5, 0.45, 0, 0],
['Myxococcus xanthus', 5, 0.55, 0, 0],
['Treponema denticola', 3, 0.05, 199.8, 5],
['Treponema denticola', 3, 0.15, 59.7, 10],
['Treponema denticola', 3, 0.25, 21.36, 11],
['Treponema denticola', 3, 0.35, 10.71, 7],
['Treponema denticola', 3, 0.45, 13.0, 2],
['Treponema denticola', 3, 0.55, 3.0, 1],
['Treponema denticola', 4, 0.05, 45.0, 6],
['Treponema denticola', 4, 0.15, 15.57, 14],
['Treponema denticola', 4, 0.25, 9.44, 9],
['Treponema denticola', 4, 0.35, 6.5, 4],
['Treponema denticola', 4, 0.45, 0, 0],
['Treponema denticola', 4, 0.55, 0, 0],
['Treponema denticola', 5, 0.05, 16.0, 4],
['Treponema denticola', 5, 0.15, 11.8, 5],
['Treponema denticola', 5, 0.25, 6.5, 2],
['Treponema denticola', 5, 0.35, 0, 0],
['Treponema denticola', 5, 0.45, 0, 0],
['Treponema denticola', 5, 0.55, 0, 0]]

def convert_results_to_latex(result):
    columns = len(result[0])
    table = Texttable()
    table.set_cols_align(["c"] * columns)
    table.set_deco(Texttable.HEADER | Texttable.VLINES)
    table.add_rows(result)
    latex_bit = latextable.draw_latex(table)
    return latex_bit

print(convert_results_to_latex(data))