import networkx as nx
from .database.DatabaseOG import Database, Data
from .clique_perc import Clique_Percolation, find_intensity
from .gen_algo import genAlgo

class Cluster:
    def __init__(self, species, PPIDb):
        self.PPIDb = PPIDb
        self.species = species
        self.query = self.PPIDb.get_interactions_by_species(self.species)
        self.Interaction_Network = self.PPIDb.get_graph(self.query)
        self.clusters = {'cliqueperc' : [], 'genalgo' : [], 'IPC': [], 'IVC':[], 'IPVC  ': []}
        self.cluster_nodes = {'cliqueperc' : [], 'genalgo' : [], 'IPC': [], 'IVC':[], 'IPVC': []}
        self.complete_graph = {'cliqueperc' : nx.Graph(),
                               'genalgo' : nx.Graph(),
                               'IPC': nx.Graph(), 
                               'IVC': nx.Graph(), 
                               'IPVC': nx.Graph()}
   
    def clusterfromAlgo(self, data, source):
        # if source == 'cliqueperc' and self.cluster_nodes['cliqueperc'] == []:
        #     pass
        # else:
        self.cluster_nodes[source] = data
        self.clusters[source] = []
        for cluster in data:
            clusterobj = nx.Graph()
            for i in range(len(cluster)):
                for j in range(i, len(cluster)):
                    if cluster[j] in self.Interaction_Network[cluster[i]].keys():
                        clusterobj.add_edge(cluster[i], cluster[j])
            self.clusters[source].append(clusterobj)
            self.complete_graph[source] = nx.compose(self.complete_graph[source], clusterobj)

    def clusterCliquePerc(self, k = 4, I = 0.05):
        self.clusterfromAlgo(Clique_Percolation(self.Interaction_Network, k, I), 'cliqueperc')
    
    def clusterGenAlgo(self, pop_size = 20, num_gens = 10, num_iters = 10, chromosome_size = 5, cluster_size = 5, 
                           elitism_rate = 0.1, mutation_rate = 0.4, num_changes = 3, tau = 0.2):
        self.clusterfromAlgo(genAlgo(self.Interaction_Network, pop_size, num_gens, num_iters, chromosome_size, 
                                     cluster_size, elitism_rate, mutation_rate, num_changes, tau).run(), 'genalgo')

    
    def clusterConsensus(self, source = 'IPC'):
        if source == 'IPC':
            self.clusterfromAlgo(Consensus([self.clusters['cliqueperc'], self.clusters['genalgo']]).IPC(), 'IPC')
        elif source == 'IPVC':
            self.clusterfromAlgo(Consensus([self.clusters['cliqueperc'], self.clusters['genalgo']]).IPVC(), 'IPVC')
        elif source == 'IVC':
            self.clusterfromAlgo(Consensus([self.clusters['cliqueperc'], self.clusters['genalgo']]).IVC(), 'IVC')

    def get_clusterCount(self, source = 'all'):
        if source == 'all':
            return len(self.getClusters())
        elif source == 'cliqueperc' or source == 'genalgo':
            return len(self.getClusters(source))

    def getClusters(self, source = 'all'):
        if source == 'all':
            return self.clusters['cliqeperc'] + self.clusters['genalgo']
        elif source == 'cliqueperc' or source == 'genalgo':
            return self.clusters[source]

    def getClusterDict(self):
        return self.clusters

    def get_cluster_size(self, source = 'all'):
        if source == 'all':
            return [len(i) for i in self.getClusters()]
        elif source == 'cliqueperc' or source == 'genalgo':
            return [len(i) for i in self.getClusters(source)]
    
    def get_cluster_nodes(self, source = 'all'):
        if source == 'all':
            return self.cluster_nodes['cliqeperc'] + self.cluster_nodes['genalgo']
        elif source == 'cliqueperc' or source == 'genalgo':
            return self.cluster_nodes[source] 
        
    def get_complete_graph(self, source = 'all'):
        if source == 'all':
            return nx.compose(self.complete_graph['cliqueperc'], self.complete_graph['genalgo'])
        else:
            return self.complete_graph[source]
        
    def cluster_call_display(self, source = 'all'):
        return self.get_complete_graph(source), self.get_cluster_nodes(self, source = 'all')
            
    def get_network(self):
        return self.Interaction_Network


# db = Database()
# cluster = Cluster('Myxococcus xanthus', db)
# cluster.clusterCliquePerc()
# cluster.clusterGenAlgo()
# cluster.clusterConsensus('IPC')
# print(cluster.getClusterDict())