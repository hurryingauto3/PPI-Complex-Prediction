from database.DatabaseOG import Database, PPIDb
from clique_perc import Clique_Percolation
from gen_algo import genAlgo
from cluster import Cluster

PPIDb = Database()
species = 'Myxococcus xanthus'
query = PPIDb.get_interactions_by_species(species)
Interaction_Network = PPIDb.get_graph(query)

clusters = Cluster(species, PPIDb)

cliqePerc = Clique_Percolation(clusters.Interaction_Network, k = 4, I = 0.05)
genAlgo = genAlgo(clusters.Interaction_Network, 20, 10, 10, 5, 5, 0.1, 0.4, 3, 0.2).run()

clusters.clusterFromPerc(cliqePerc)
clusters.clusterFromGen(genAlgo)

clusters.get