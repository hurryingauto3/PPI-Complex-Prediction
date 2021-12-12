import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class PPIN:
    
    graph = nx.Graph()
    file_data = []

    def __init__(self, file):
        
        """Takes in a file and converts it 
        to type PPIN using the Networkx Library"""
    
        self.read_file(file)
        self.get_graph()

    def read_file(self, file):
        """Reads in a file and returns a list of lines"""
        f = open(file, 'r')
        self.file_data = f.read()
        # print(self.file_data)
        self.file_data = self.file_data.split("\n")
        # print(self.file_data)
        f.close()

    def display(self):
        nx.draw(self.graph, pos=nx.spring_layout(self.graph))
        
    def get_graph(self):
        """Converts the file data into a graph"""
        # print(type(self.file_data))
        for line in self.file_data:
            if len(line) == 0:
              continue
            line = line.split("\t")
            self.graph.add_edge(line[0], line[1])

    def get_nodes(self):
        """Returns a list of nodes in the graph"""
        return self.graph.nodes()

if __name__ == "__main__":
    ppin_obj = PPIN("./Datasets/Test_space_screens-19-1159.tsv")