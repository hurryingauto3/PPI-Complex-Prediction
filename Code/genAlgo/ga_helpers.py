# TODO: - integrate actual data



import networkx as nx 
import numpy as np
import matplotlib.pyplot as plt
import random

from evolalgo import Chromosome

nodes = ['a', 'b', 'c', 'd', 'e', 'f']
edges = [('a','b'), ('a','c'), ('a', 'd'), ('b','c'), ('b','d') , ('c','e'),  ('e','f'), ('e','g'), ('f', 'g')]

sample = nx.Graph()
sample.add_nodes_from(nodes)
sample.add_edges_from(edges)

# sub = sample.subgraph(['a','b','c', 'd'])
# print(sub.edges)
# print(sample.edges(nbunch=['a', 'c']))



class genAlgo(object):
    def __init__(self, ppin_graph: nx.Graph, pop_size: int, n_offspring: int, num_gens: int, num_iters: int,
                chromosome_size: int, cluster_size: int):
        self.ppin_graph = ppin_graph
        self.pop_size = pop_size
        self.n_offspring = n_offspring
        self.num_gens = num_gens
        self.num_iters = num_iters
        self.chromosome_size = chromosome_size
        self.cluster_size = cluster_size 
        self.initialize_pop()

    
    def generate_chromosome(self) -> list:
        """create a chromosome which is a list of clusters 

        Args:
            chromosome_size (int): number of clusters in each chromosome 
            cluster_size (int): number of nodes in each cluster
        """
        n = self.ppin_graph.number_of_nodes()
        chromosome = []
        for i in range(self.chromosome_size): 
            chromosome.append(random.sample(list(range(n+1)), k=self.cluster_size))
        return chromosome

    
    def initialize_pop(self) -> None:
        self.population = {}
        for i in range(self.pop_size):
            chrom = self.generate_chromosome(chrom)
            self.population[chrom] =  self.eval_fitness(chrom) 
    
    
    def indices2nodes(self, cluster: list) -> list:
        nodes = list(self.ppin_graph.nodes)
        cluster_nodes = []
        for idx in cluster:
            cluster_nodes.append(nodes[idx])
        return cluster_nodes
   
    
    def compute_w_ik(self, cluster_nodes: list) -> int:
        w_ik = 0
        for u in self.ppin_graph.nodes:
            if u in cluster_nodes:
                continue 
            else:
                for v in cluster_nodes:
                    if self.ppin_graph.has_edge(u,v):
                        w_ik += 1
        return w_ik


   
    def eval_fitness(self, chromosome: list) -> float:
        fitness = 0
        for cluster in chromosome:
            cluster_nodes = self.indices2nodes(cluster)
            cluster_graph = self.ppin_graph.subgraph(cluster_nodes)
            
            # compute three metrics
            w_kk = cluster_graph.number_of_edges()
            a_k = (self.cluster_size**2 + self.cluster_size) / 2
            w_ik = self.compute_w_ik(cluster_nodes)
            fitness += ((w_kk) / (a_k + w_ik))
        
        return fitness 
            

    def eval_fitness_all(self) -> None:
        for chromosome in self.population:
            fitness = self.eval_fitness(chromosome)
            self.population[chromosome] = fitness



# print(generate_chrom(sample, 20, 5))
# print(random.sample(list(range(50)), k=10))