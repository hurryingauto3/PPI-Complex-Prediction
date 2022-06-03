from database.DatabaseOG import Database, PPIDb
from cluster import Cluster

PPIDb = Database()
species = 'Myxococcus xanthus'
query = PPIDb.get_interactions_by_species(species)
Interaction_Network = PPIDb.get_graph(query)

clusters = Cluster(species, PPIDb)
clusters.clusterCliquePerc()
clusters.clusterGenAlgo()
