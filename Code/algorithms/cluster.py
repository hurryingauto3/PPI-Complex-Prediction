import networkx as nx
from database.DatabaseOG import Database, Data
from clique_perc import Clique_Percolation, find_intensity
from gen_algo import genAlgo

class Cluster:
    def __init__(self, species, PPIDb):
        self.PPIDb = PPIDb
        self.species = species
        self.query = self.PPIDb.get_interactions_by_species(self.species)
        self.Interaction_Network = self.PPIDb.get_graph(self.query)
        self.clusters = {}
        self.cluster_nodes = {}
   
    def clusterfromAlgo(self, data, source):
        self.clusters[source] = []
        for i in self.query:
            for j in data:
                clusterobj = nx.Graph()
                for k in j:
                    for l in j:
                        if i['Gene A'] == k and i['Gene B'] == l or i['Gene B'] == l and i['Gene A'] == k:
                            clusterobj.add_edge(k, l)
                self.clusters[source].append(clusterobj)

    def clusterCliquePerc(self):
        self.clusterfromAlgo(Clique_Percolation(self.Interaction_Network, k = 4, I = 0.05), 'cliqueperc')
    
    def clusterGenAlgo(self):
        self.clusterfromAlgo(genAlgo(self.Interaction_Network, 20, 10, 10, 5, 5, 0.1, 0.4, 3, 0.2).run(), 'genalgo')

    def get_clusterCount(self, source = 'all'):
        if source == 'all':
            return len(self.getClusters())
        elif source == 'cliqueperc' or source == 'genalgo':
            return len(self.get_clusters(source))

    def getClusters(self, source = 'all'):
        if source == 'all':
            return self.clusters['cliqeperc'] + self.clusters['genalgo']
        elif source == 'cliqueperc' or source == 'genalgo':
            return self.clusters[source]
    
    def get_cluster_size(self, source = 'all'):
        if source == 'all':
            return [len(i) for i in self.get_clusters()]
        elif source == 'cliqueperc' or source == 'genalgo':
            return [len(i) for i in self.get_clusters(source)]
            
    def get_network(self):
        return self.Interaction_Network
    