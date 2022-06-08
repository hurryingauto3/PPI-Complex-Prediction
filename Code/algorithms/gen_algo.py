# TODO: - fix bug in mutate
#       - integrate actual data
import networkx as nx 
import numpy as np
import matplotlib.pyplot as plt
import random
import time 

class genAlgo(object):
    def __init__(self, ppin_graph: nx.Graph, pop_size: int, num_gens: int, num_iters: int,
                chromosome_size: int, cluster_size: int, elitism_rate: float, mutation_rate: float, 
                num_changes: int, tau: int):
        self.ppin_graph = ppin_graph
        self.pop_size = pop_size
        self.num_gens = num_gens
        self.num_iters = num_iters
        self.chromosome_size = chromosome_size
        self.cluster_size = cluster_size 
        self.elitism_rate = elitism_rate
        self.mutation_rate = mutation_rate
        self.num_changes = num_changes
        self.tau = tau
        # self.initialize_pop()

    
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
            self.population[chrom] = self.eval_fitness(chrom) 
    
    
    def indices2nodes(self, cluster: list) -> list:
        nodes = list(self.ppin_graph.nodes)
        # print(cluster)
        # print(nodes)
        cluster_nodes = []
        for idx in cluster:
            # print(idx)
            cluster_nodes.append(nodes[idx])
        return cluster_nodes


    def nodes2indices(self, cluster: list) -> list:
        nodes = list(self.ppin_graph.nodes)
        cluster_idx = []
        for node in cluster:
            cluster_idx.append(nodes.index(node))
        return cluster_idx

    
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
            # print(r)
            s = 0
            # while s < r:
            for chromosome in self.population:
                # print(cum_sums[chromosome][1])
                s += cum_sums[chromosome][1]
                if s >= r:
                    other_parents.append(chromosome)
                    break     
        return elitism_parents, other_parents


    def chrom2list(self, chromosome: tuple) -> list:
        chromosome = list(chromosome)
        for j in range(len(chromosome)):
            chromosome[j] = list(chromosome[j])
        return chromosome
        
    def chromlist2tup(self, chromosome: list) -> tuple:
        for j in range(len(chromosome)):
            chromosome[j] = tuple(chromosome[j])
        chromosome = tuple(chromosome)
        return chromosome


# debug this to remove repeating nodes
    def mutate_util(self, chromosome: tuple, i: int, k: int):
        chromosome = self.chrom2list(chromosome)
        rand = random.randrange(0, len(chromosome))
        chromosome[rand].append(chromosome[i][k])
        chromosome[i].remove(chromosome[i][k])
        chromosome = self.chromlist2tup(chromosome)
        # print(chromosome)
        return chromosome

    def mutate_util2(self, chromosome: tuple, i: int, k: int):
        chromosome = self.chrom2list(chromosome)
        cluster = self.indices2nodes(chromosome[i]) 
        selected_node = cluster[k]
        adjacents = self.nodes2indices(list(self.ppin_graph.neighbors(selected_node)))
        cluster = self.nodes2indices(cluster)
        adjacents = [adjacents[i] for i in range(len(adjacents)) if adjacents[i] not in cluster]
        chromosome[i].extend(adjacents)
        chromosome = self.chromlist2tup(chromosome)
        # print(chromosome)
        return chromosome


    def mutate(self, chromosome: dict):
        # print(chromosome)
        for i in range(len(chromosome)):
            r_1 = random.random()
            if r_1 < self.mutation_rate:
                for _ in range(self.num_changes):
                    r_2 = random.random()
                    # print(chromosome)
                    k = random.randrange(0, len(chromosome[i])) 
                    if r_2 < self.tau:
                        chromosome = self.mutate_util(chromosome, i, k)
                    else: 
                        chromosome = self.mutate_util2(chromosome, i, k)
        return chromosome


    def create_offspring(self) -> dict:
        elitism_parents, other_parents = self.select_parent()
        offspring = []
        for parent in other_parents:
            offspring.append(self.mutate(parent))
        offspring.extend(elitism_parents)
        new_pop = {}
        for child in offspring:
            new_pop[child] = 0
        return new_pop 

    def format_output(self, clustering):
        cluster_nodes = []
        for cluster in clustering:
            cluster_nodes.append(self.indices2nodes(cluster))
        return cluster_nodes   


    def run(self):
        start = time.time()
        best_chromosomes = []
        for iter in range(self.num_iters):
            # initialize_pop
            self.initialize_pop()
            gen = 0
            while gen <= self.num_gens:
                self.population = self.create_offspring()
                self.eval_fitness_all()
                gen += 1
            best_c = max(self.population, key= lambda key: self.population[key])
            best_chromosomes.append((best_c, self.eval_fitness(best_c)))
        # choose single best clustering from best chromosomes
        final_clustering = max(best_chromosomes, key = lambda key: best_chromosomes[1])
        # final_clustering = self.chrom2list(final_clustering[0])
        final_clustering = final_clustering[0]
        # print(final_clustering)
        print("Time taken to execute clustering via Genetic Algorithm: ", time.time() - start)
        return self.format_output(final_clustering)


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

    