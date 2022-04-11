import itertools
import json
import networkx as nx 

complexes_path = '../Datasets/coreComplexes.json'


class Cluster:
    def __init__(self, pubmed_id: str, proteins: list):
        # pubmed id, proteins 
        self.populate_complex(pubmed_id, proteins)
        self.create_graph()

    def populate_complex(self, pubmed_id: str, proteins: list):
        self.pubmed_id = pubmed_id
        self.proteins = proteins

    def create_graph(self):
        self.complex = nx.Graph()
        self.complex.add_nodes_from(self.proteins)
        self.complex.add_edges_from(itertools.combinations(self.proteins, 2))
        print(self.complex.edges)


def read_file(path): 
    f = open(path)
    complex_data = json.load(f)
    f.close()
    return complex_data

def parse_data(complex_data):
    clusters = []
    for complex in complex_data:
        pubmed_id = complex['PubMed ID']
        proteins = complex["subunits(UniProt IDs)"].split(';')
        cluster = Cluster(pubmed_id, proteins)
        clusters.append(cluster)
    return clusters
         

######### FEATURE EXTRACTION 





if __name__ == "__main__":
    complex_data = read_file(complexes_path)
    parse_data(complex_data)