import networkx as nx
import matplotlib.pyplot as plt
import Database as PPIdb

class PPIN:   
    graph = nx.Graph()
    def __init__(self, db):
        """Takes in a file and converts it 
        to type PPIN using the Networkx Library"""
        self.get_graph_from_db(db)
        self.display()

    # def get_graph_from_file(self, file):
    #     """Reads in a file and returns a list of lines"""
    #     f = open(file, 'r')
    #     for line in f.read().split("\n"):
    #         if len(line) == 0:
    #           continue
    #         line = line.split("\t")
    #         self.graph.add_edge(line[0], line[1])
    #     f.close()

    def get_graph_from_db(self, db):
        for i in db.get_interactions():
            self.graph.add_edge(i["geneA"], i["geneB"])
        
    def display(self):
        nx.draw(self.graph, pos=nx.spring_layout(self.graph), with_labels=True)
        plt.show()
        
    def get_prots(self):
        """Returns a list of nodes in the graph"""
        return self.graph.nodes()
    
    def get_interactions(self):
        """Returns a list of interactions for a given protien"""
        return self.graph.edges()
    
if __name__ == "__main__":
    
    ppidb = PPIdb.Database()
    PPIN = PPIN(ppidb)