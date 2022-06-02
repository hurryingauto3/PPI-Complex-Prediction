import networkx as nx
from .database.DatabaseOG import Database, Data
from .clique_perc import Clique_Percolation, find_intensity
from .evolalgo import Chromosome, evolAlgo

class Cluster:
    def __init__(self):
        self.Interaction_Network = nx.Graph
        self.list_of_clusters = []
    # def __init__(self, source, specie_query, PPIDb) -> None:
    #     self.Interaction_Network = nx.Graph
    #     self.list_of_clusters = []
    #     if source == 'perc':
    #         self.clusterFromPerc(specie_query, PPIDb)
    #         self.clusterSource = 'perc'
    #     elif source == 'gen':
    #         self.clusterFromGen(specie_query, PPIDb)
    #         self.clusterSource = 'gen'
    #     elif source == 'gnn':
    #         # self.clusterFromGNN(specie_query, PPIDb)
    #         self.clusterSource = 'gnn'
    #     else:
    #         raise ValueError('Invalid source')
        
    def clusterFromPerc(self, specie_query, PPIDb, k = 4, I = 0.05):
        query = PPIDb.get_interactions_by_species(specie_query)
        self.Interaction_Network = PPIDb.get_graph(query)
        self.list_of_clusters = Clique_Percolation(self.Interaction_Network, k, I)
        self.clusterSource = 'perc'

    def clusterFromGen(self, specie_query, PPIDb):
        query = PPIDb.get_interactions_by_species(specie_query)
        self.Interaction_Network = PPIDb.get_graph(query)
    
    def get_cluster_size(self):
        pass

    def cluster_edges(self):
        pass

    def cluster_nodes(self):
        nodes = []
        for cluster in self.list_of_clusters:
            for node in cluster:
                nodes.append(node)

    def get_cluster_source(self):
        return self.clusterSource

    def get_network(self):
        return self.Interaction_Network
    
    def get_clusters(self):
        return self.list_of_clusters
