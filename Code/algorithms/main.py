from database.DatabaseOG import Database
from cluster import Cluster

PPIDb = Database()
species = 'Myxococcus xanthus'
query = PPIDb.get_interactions_by_species(species)
Interaction_Network = PPIDb.get_graph(query)

clusters = Cluster(species, PPIDb)
clusters.clusterCliquePerc()
print(clusters.getClusters('cliqueperc'))
clusters.clusterGenAlgo()
print(clusters.getClusters('genalgo'))