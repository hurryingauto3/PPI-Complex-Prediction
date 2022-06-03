from .database.DatabaseOG import Database, Data
from .cluster import Cluster

class Master:
    def __init__(self):
        self.PPIDb = Database()
        self.cluster_species = {}
        
    def add_specie(self, specie):
        if specie not in self.cluster_species.keys():
            self.cluster_species[specie] = Cluster(specie, self.PPIDb)
        
    def add_perc_for_specie(self, specie, k = 4, I = 0.05):
        self.add_specie(specie)
        self.cluster_species[specie].clusterCliquePerc(k, I)
            
    def add_gen_for_specie(self, specie):
        self.add_specie(specie)
        self.cluster_species[specie].clusterGenAlgo()
        
    def get_specie_interactions(self, specie):
        self.add_specie(specie)
        return self.cluster_species[specie].get_network()
        
    def get_specie_clusters(self, specie, source = 'all'):
        return self.cluster_species[specie].getClusters(source)
    
    def get_specie_cluster_nodes(self, specie, source = 'all'):
        return self.cluster_species[specie].get_cluster_nodes(source)
    
    def get_specie_cluster_graph(self, specie, source = 'all'):
        return self.cluster_species[specie].get_complete_graph(source)
    
    def get_specie_display(self, specie, source = 'all'):
        return self.cluster_species[specie].cluster_call_display(source)
    
    def get_database(self):
        return self.PPIDb
    
    def get_taxons(self, limit = -1):
        return list(self.PPIDb.get_all_taxons(limit))
        
    
    