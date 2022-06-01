# TODO: - finish elitism selection
#           - figure out while loop situation
#       - code mutation
#       - main run function
#       - integrate actual data


import networkx as nx 
import numpy as np
import matplotlib.pyplot as plt
import random


nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
edges = [('a','b'), ('a','c'), ('a', 'd'), ('b','c'), ('b','d') , ('c','e'),  ('e','f'), ('e','g'), ('f', 'g'), ('a', 'g')]

sample = nx.Graph()
sample.add_nodes_from(nodes)
sample.add_edges_from(edges)

# sub = sample.subgraph(['a','b','c', 'd'])
# print(sub.edges)
# print(sample.edges(nbunch=['a', 'c']))


class genAlgo(object):
    def __init__(self, ppin_graph: nx.Graph, pop_size: int, n_offspring: int, num_gens: int, num_iters: int,
                chromosome_size: int, cluster_size: int, elitism_rate: float):
        self.ppin_graph = ppin_graph
        self.pop_size = pop_size
        self.n_offspring = n_offspring
        self.num_gens = num_gens
        self.num_iters = num_iters
        self.chromosome_size = chromosome_size
        self.cluster_size = cluster_size 
        self.elitism_rate = elitism_rate
        self.initialize_pop()

    
    def generate_chromosome(self) -> tuple:
        """create a chromosome which is a list of clusters 

        Args:
            chromosome_size (int): number of clusters in each chromosome 
            cluster_size (int): number of nodes in each cluster
        """
        n = self.ppin_graph.number_of_nodes()
        chromosome = []
        for i in range(self.chromosome_size): 
            chromosome.append(tuple(random.sample(list(range(n)), k=self.cluster_size)))
        return tuple(chromosome)

    
    def initialize_pop(self) -> None:
        self.population = {}
        for i in range(self.pop_size):
            chrom = self.generate_chromosome()
            chrom = tuple(chrom)
            self.population[chrom] =  self.eval_fitness(chrom) 
    
    
    def indices2nodes(self, cluster: list) -> list:
        nodes = list(self.ppin_graph.nodes)
        # print(nodes)
        cluster_nodes = []
        for idx in cluster:
            # print(idx)
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


   
    def eval_fitness(self, chromosome: tuple) -> float:
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
            
    

    def select_parent(self) -> tuple:
        sorted_pop = dict(sorted(self.population.items(), key=lambda item: item[1])) 
        elitism_size = int(self.elitism_rate*self.pop_size)
        elitism_parents =  {k: sorted_pop[k] for k in list(sorted_pop)[-elitism_size:]}
        # print(elitism_parents)
        cum_sums = cumsum(sorted_pop)
        S = list(cum_sums.values())[-1][1]
        N = self.pop_size - len(elitism_parents)
        other_parents = []
        for i in range(N):
            r = random.uniform(0, S)
            print(r)
            s = 0
            # while s < r:
            for chromosome in self.population:
                # print(cum_sums[chromosome][1])
                s += cum_sums[chromosome][1]
                if s >= r:
                    other_parents.append(chromosome)
                    break     
        return elitism_parents, other_parents

    def mutate(self, chromosome):
        pass 

    def run(self):
        pass


def cumsum(pop: dict) -> dict:
    cum = 0
    cum_pop = {}
    chroms = list(pop.keys())
    fitnesses = list(pop.values())
    for i in range(len(chroms)):
        cum += fitnesses[i]
        cum_pop[chroms[i]] = (fitnesses[i], cum)
    # print(cum_pop)
    return cum_pop

    
ga_instance = genAlgo(sample, 50, 10, 5, 5, 10, 3, 0.1)
# print(ga_instance.population)
ga_instance.select_parent()

# x = {1:3, 2:12, 3:9, 4:4, 5:10}

# x_sort = dict(sorted(x.items(), key=lambda item: item[1]))
# print(x_sort)
# x_sel = {k: x_sort[k] for k in list(x_sort)[:2]}
# print(x_sel)

# rand_dic = {'a': 4, 'b':2, 'c': 10, 'd': 8, 'e': 11, 'f': 12}
    # i     pass 
# print(list(rand_dic.keys()).index("d"))
# cum = cumsum(rand_dic)
# print(max([x[1] for x in cum.values()]))
# print(list(cum.values())[-1][1])
# print(cum)
# print(max(cum, key=lambda key: ))
# for key in cum:
    # print(cum[key][1])