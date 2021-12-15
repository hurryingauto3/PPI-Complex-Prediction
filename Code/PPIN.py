import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pymongo import database
import pyrebase
from firebaseConfig import config

class PPIN:   
    PPIdb = pyrebase.initialize_app(config)
    graph = nx.Graph()
    file_data = []
    def __init__(self, input, type = "db"):
        
        """Takes in a file and converts it 
        to type PPIN using the Networkx Library"""
        if type == "db":
            self.PPIdb = input
            
        elif type == "file":
            self.get_graph_from_file(input)

    def get_graph_from_file(self, file):
        """Reads in a file and returns a list of lines"""
        f = open(file, 'r')
        for line in f.read().split("\n"):
            if len(line) == 0:
              continue
            line = line.split("\t")
            self.graph.add_edge(line[0], line[1])
        f.close()

    def get_graph_from_db(self, protien):
        pass
        
    def display(self):
        nx.draw(self.graph, pos=nx.spring_layout(self.graph))

    def get_prots(self):
        """Returns a list of nodes in the graph"""
        return self.graph.nodes()
    
    def get_interactions(self):
        """Returns a list of interactions for a given protien"""
        return self.graph.edges()
    
    def get_kMeansCluster(self):
        """Returns a list of kMeans clusters for a given protien"""
        pass

    def get_MCLCluster(self):
        """Returns a list of MCL clusters for a given protien"""
        pass

if __name__ == "__main__":
    ppi = PPIN("MDH2")
    print(ppi.get_interactions())
    # print(nx.clustering(ppi.graph))