from algorithms.master import Cluster
from algorithms.database.DatabaseOG import Database
import pandas as pd

species = 'Myxococcus xanthus'#, 'Treponema denticola']
mutation = [0.4, 0.5, 0.6, 0.7, 0.8]
intensity = [0.05, 0.15, 0.25, 0.35, 0.45]

db = Database()
resultCliqe = []
resultGA = []
resultCon = []

cluster = Cluster(species, db)

# def getAvgEdgeWeight(graph):
#     edgesum = 0
#     for i in graph.edges(data=True):
#         print(i[2])
#     return edgesum/len(graph.edges)

# def getAvgNeighbor(graph):
#     return sum(graph.degree())/len(graph.nodes)

for j in range(len(mutation)):
    cluster.clusterCliquePerc(I = intensity[j])
    cluster.clusterGenAlgo(mutation_rate = mutation[j])
    cluster.clusterConsensus('IPC')
    
    if cluster.get_clusterCount('cliqueperc') > 0:
        
        resultCliqe.append([species, intensity[j], 
        round(sum(cluster.get_cluster_size('IPC'))/len(cluster.get_cluster_size('cliqueperc')),2), cluster.get_clusterCount('cliqueperc')])
    else:
        resultCliqe.append([species, intensity[j], 0, 0, 0, 0])

    if cluster.get_clusterCount('genalgo') > 0:
        resultGA.append([species, intensity[j], 
        round(sum(cluster.get_cluster_size('genalgo'))/len(cluster.get_cluster_size('genalgo')),2), cluster.get_clusterCount('genalgo')])
    
    else:
        resultGA.append([species, intensity[j], 0, 0, 0, 0])

    if cluster.get_clusterCount('IPC') > 0:
        resultCon.append([species, getAvgEdgeWeight(cluster.get_complete_graph('IPC')), getAvgNeighbor(cluster.get_complete_graph('IPC')), 
        round(sum(cluster.get_cluster_size('IPC'))/len(cluster.get_cluster_size('IPC')),2), cluster.get_clusterCount('IPC')])
    else:
        resultCon.append([species, intensity[j], mutation[j], 0, 0, 0, 0])

print('Clique perc:', resultCliqe)
print('Gen Algo:', resultGA)    
print('Consensus:', resultCon)