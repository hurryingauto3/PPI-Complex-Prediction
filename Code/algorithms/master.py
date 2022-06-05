from .database.DatabaseOG import Database, Data
from .cluster import Cluster
import numpy as np
from tabulate import tabulate
from texttable import Texttable
import latextable

class Master:
    def __init__(self):
        self.PPIDb = Database()
        self.cluster_species = {}
        # for x in list(self.PPIDb.get_all_taxons(30)):
        #     specie = x['Species Name']
        #     self.cluster_species[specie] = Cluster(specie, self.PPIDb)
        #     print("Added: " + specie)
        
    def add_specie(self, specie):
        if specie not in self.cluster_species.keys():
            self.cluster_species[specie] = Cluster(specie, self.PPIDb)
        
    def add_perc_for_specie(self, specie, k = 4, I = 0.05):
        self.add_specie(specie)
        self.cluster_species[specie].clusterCliquePerc(k, I)
            
    def add_gen_for_specie(self, specie, pop_size = 20, num_gens = 10, num_iters = 10, chromosome_size = 5, cluster_size = 5, 
                           elitism_rate = 0.1, mutation_rate = 0.4, num_changes = 3, tau = 0.2):
        self.add_specie(specie)
        self.cluster_species[specie].clusterGenAlgo(pop_size, num_gens, num_iters, chromosome_size, 
                                     cluster_size, elitism_rate, mutation_rate, num_changes, tau)
        
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
    
    def get_consensus(self, specie):
        return self.cluster_species[specie].get_consensus()
    
    def get_all_results_perc(self, k, I):
        result = [[""]]
        for specie in ['Myxococcus xanthus', 'Homo sapiens', 'Treponema denticola']:
            for k in range(3, 6):
                result[0].append(k)
                for I in np.arange(0.05, 0.6, 0.1):
                    self.add_perc_for_specie(specie, k, I)
                    cluster_size = self.cluster_species[specie].get_cluster_size('cliqueperc')
                    cluster_count = self.cluster_species[specie].get_clusterCount('cliqueperc')
                    result.append([specie, I, cluster_size, cluster_count])  
        return result      
    
    def get_all_result_gen(self, pop_size, num_gens, num_iters, chromosome_size, cluster_size, 
                           elitism_rate, mutation_rate, num_changes, tau):
        pass
    
    def convert_results_to_latex(self, result):
        columns = len(result[0])
        table = Texttable()
        table.set_cols_align(["c"] * columns)
        table.set_deco(Texttable.HEADER | Texttable.VLINES)
        table.add_rows(result)
        latex_bit = latextable.draw_latex(table)
        return latex_bit
        
    #pop_size: int, num_gens: int, num_iters: int,
                # chromosome_size: int, cluster_size: int, elitism_rate: float, mutation_rate: float, 
                # num_changes: int, tau: int
    # def get_all_results(self):
    #     for x in list(PPIDb.get_all_taxons()):
    #         specie = x['Species Name']
    #         self.add_perc_for_specie(specie)
    #         self.add_gen_for_specie(specie)
        
        
    
    