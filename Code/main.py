from algorithms.master import Cluster
from algorithms.database.DatabaseOG import Database
import pandas as pd

species = ['Myxococcus xanthus']#, 'Treponema denticola']
mutation = [0.4, 0.5, 0.6, 0.7, 0.8]
db = Database()
# result = []
# for i in range(len(species)):
#     cluster = Cluster(species[i], db)
#     for j in range(len(mutation)):
#         cluster.clusterGenAlgo(20, 10, 5, 5, 5, 0.1, mutation[j], 3, 0.2)
#         print(cluster.clusters['genalgo'])
#         if cluster.get_clusterCount('genalgo') > 0:
#             result.append([species[i], mutation[j], round(sum(cluster.get_cluster_size('genalgo'))/len(cluster.get_cluster_size('genalgo')),2), cluster.get_clusterCount('genalgo')])
#         else:
#             result.append([species[i], mutation[j], 0, 0])
# print(result)

query = db.get_interactions_by_species('Myxococcus xanthus')
g = db.get_graph(query)