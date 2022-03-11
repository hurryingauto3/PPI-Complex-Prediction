import networkx as nx
import matplotlib.pyplot as plt
import DatabaseOG as PPIdb
from pyvis.network import Network

class PPIN:   
    graph = nx.Graph()
    def __init__(self, db):
        """Takes in a file and converts it 
        to type PPIN using the Networkx Library"""
        self.get_graph_from_db(db)
        self.display()

    def get_graph_from_db(self, db):
        for i in db.get_interactions():
            self.graph.add_edge(i["Gene A"], i["Gene B"])
        
    def display(self):
        net = Network(notebook=True, bgcolor="#222222", font_color="white", height="100%", width="100%")
        net.from_nx(self.graph)
        net.show("PPIN.html")
        # nx.draw(self.graph, pos=nx.spring_layout(self.graph), with_labels=True)
        # plt.show()
        
    def get_prots(self):
        """Returns a list of nodes in the graph"""
        return self.graph.nodes()
    
    def get_interactions(self):
        """Returns a list of interactions for a given protien"""
        return self.graph.edges()
    
if __name__ == "__main__":
    
    ppidb = PPIdb.Database()
    PPIN = PPIN(ppidb)
    print(PPIN.get_interactions())