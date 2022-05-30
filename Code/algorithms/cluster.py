import networkx as nx

class Cluster:

    cluster = nx.Graph()

    def __init__(self, source) -> None:
        if source == 'perc':
            self.clusterFromPerc()
            self.clusterSource = 'perc'
        elif source == 'gen':
            self.clusterFromGen()
            self.clusterSource = 'gen'
        elif source == 'gnn':
            self.clusterFromGNN()
            self.clusterSource = 'gnn'
        else:
            raise ValueError('Invalid source')
        
    def clusterFromGen(self):
        pass

    def clusterFromPerc(self):
        pass

    def clusterFromGNN(self):
        pass
    
    def get_cluster_size(self):
        pass

    def cluster_edges(self):
        pass

    def cluster_nodes(self):
        pass

    def get_cluster_source(self):
        return self.clusterSource

    def sendToFrontend(self):
        return self.cluster
