# Class of generic evolutionary algorithm
from logging import error
import random as rd
import numpy as np
import matplotlib.pyplot as plt

class Chromosome:
    def __init__(self, id, genes, fitness) -> None:
        self.id = id
        self.genes = genes
        self.fitness = fitness

class evolAlgo:
    @staticmethod
    def __init__(self, fileName, nPop, nOffSpring, nGen, rMutation, nIter, pSel, sSel, minimize):

        self.fileData = self.readFile(fileName)
        # Initialize parameters
        self.nPop = nPop
        self.nOffSpring = nOffSpring
        self.nGen = nGen
        self.rMutation = rMutation
        self.nIter = nIter
        self.pSel = pSel
        self.sSel = sSel
        self.minimize = minimize
        # Initialize population
        self.population = []
        self.parents = []
        self.survivors = []
        # Statistics
        self.bestFitnesses = []
        self.avgFitnesses = []

    def readFile(self, fileName):
        f = open(fileName, "r")
        lines = f.readlines()
        f.close()
        return lines

    def mutation(self, chromosomes):
        for i in range(len(chromosomes)):
            if rd.random() < self.rMutation:
                np.random.shuffle(chromosomes[i].genes)

    def crossover(self):
        offSpring = []
        while(len(offSpring) < self.nOffSpring):
            p1 = rd.choice(self.parents)
            p2 = rd.choice(self.parents)
            if p1 != p2:
                p1Genes = list(p1.genes[0:int(len(p1.genes)//2)])
                p2Genes = list(p2.genes[int(len(p2.genes)//2):len(p2.genes)])
                chromosome = p1Genes + p2Genes
                offSpring.append(Chromosome(0, chromosome, self.compFitness(chromosome)))

                p1Genes = list(p2.genes[0:int(len(p2.genes)//2)])
                p2Genes = list(p1.genes[int(len(p1.genes)//2):len(p1.genes)])
                chromosome = p1Genes + p2Genes
                offSpring.append(Chromosome(0, chromosome, self.compFitness(chromosome)))

            else:
                continue
        self.mutation(offSpring)
        for i in range(len(offSpring)):
            offSpring[i].id = self.nPop + i
        self.population.extend(offSpring)

    def parentSelection(self):
        if self.pSel == "fp":
            self.parents = self.fitnessProp(self.nOffSpring)
        elif self.pSel == "rb":
            self.parents = self.rankBased(self.nOffSpring)
        elif self.pSel == "bt":
            self.parents = self.binaryTournament(self.nOffSpring)
        elif self.pSel == "tr":
            self.parents = self.truncation(self.nOffSpring)
        elif self.pSel == "rd":
            self.parents = self.random(self.nOffSpring)
        else:
            error("Invalid parent selection scheme")

    def survivalSelection(self):
        if self.sSel == "fp":
            self.survivors = self.fitnessProp(self.nPop)
        elif self.sSel == "rb":
            self.survivors = self.rankBased(self.nPop)
        elif self.sSel == "bt":
            self.survivors = self.binaryTournament(self.nPop)
        elif self.sSel == "tr":
            self.survivors = self.truncation(self.nPop)
        elif self.sSel == "rd":
            self.survivors = self.random(self.nPop)
        else:
            error("Invalid survival selection scheme")

    # Selection schemes for parent and survivor selection

    def fitnessProp(self, N):
        fitnessSum = sum([i.fitness for i in self.population])
        if self.minimize:
            fitnessProb = [1 - ((fitnessSum-i.fitness)/fitnessSum) for i in self.population]
        else:
            fitnessProb = [i.fitness/fitnessSum for i in self.population]

        return list(np.random.choice(self.population, N, p=fitnessProb, replace=False))

    def rankBased(self, N):
        
        sortedFitness = self.sortFitness() 
        fitnessProb = [i/self.nPop for i in range(len(sortedFitness))]
        fitnessProb = [i/sum(fitnessProb) for i in fitnessProb]
        if self.minimize:
            fitnessProb = fitnessProb[::-1]
        return list(np.random.choice(sortedFitness, N, p=fitnessProb, replace=False))

    def binaryTournament(self, N):
        finalPopulation = []
        while(len(finalPopulation) < N):
            c1 = rd.choice(self.population)
            c2 = rd.choice(self.population)
            
            if c1.fitness > c2.fitness and self.minimize == False:
                if c1 in finalPopulation:
                    continue
                finalPopulation.append(c1)
            elif c1.fitness < c2.fitness and self.minimize == False:
                if c2 in finalPopulation:
                    continue
                finalPopulation.append(c2)
            elif c1.fitness > c2.fitness and self.minimize == True:
                if c2 in finalPopulation:
                    continue
                finalPopulation.append(c2)
            elif c1.fitness < c2.fitness and self.minimize == True:
                if c1 in finalPopulation:
                    continue
                finalPopulation.append(c1)

        return finalPopulation

    def truncation(self, N): 
        if self.minimize:
            return self.sortFitness()[:N]
        else:
            return self.sortFitness()[-N:]
    def random(self, N): return list(
        np.random.choice(self.population, N, replace=False))

    def compFitnessAll(self):
        for i in range(self.nPop):
            self.population[i].fitness = self.compFitness(
                self.population[i].genes)

    def sortFitness(self): return sorted(self.population, key=lambda x: x.fitness)

    def bestFitness(self): 
        if self.minimize:
            return min([i.fitness for i in self.population])
        else:
            return max([i.fitness for i in self.population])

    def avgFitness(self): return sum([i.fitness for i in self.population])/self.nPop

    def plot(self, fitness, name):
        plt.plot(self.bestFitnesses)
        plt.plot(self.avgFitnesses)
        plt.xlabel("Generation")
        plt.ylabel("Fitness" + " (" +fitness + ")")
        plt.legend(["Average Best Fitness over " + str(self.nIter) + " iterations",
                    "Average Fitness over " + str(self.nIter) + " iterations"])
        plt.savefig(name+".png")
        plt.close()
    def run(self):
        for i in range(self.nGen):
            self.popInit()
            bestFitness = 0
            avgFitness = 0
            for j in range(self.nIter):
                # print("Old Gen", [i.fitness for i in self.population])
                self.parentSelection()
                self.crossover()
                # print("w/Offspring", [i.fitness for i in self.population])
                self.compFitnessAll()
                self.survivalSelection()
                # print("Survivors", [i.fitness for i in self.survivors], '\n')
                self.population = self.survivors
                self.survivors = []

                bestFitness += self.bestFitness()
                avgFitness += self.avgFitness()

            self.bestFitnesses.append(bestFitness/self.nIter)
            self.avgFitnesses.append(avgFitness/self.nIter)
