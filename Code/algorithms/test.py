from itertools import count
from urllib.error import HTTPError
from itsdangerous import NoneAlgorithm
from database.DatabaseOG import Database, Data
from clique_perc import Clique_Percolation, find_intensity
import urllib.parse
import urllib.request
import requests
import json
import time
import pandas as pd
from Bio import Entrez
import requests, sys
import numpy as np
from matplotlib.font_manager import json_load
from pyvis.network import Network
import itertools
import seaborn as sns
import plotly.express as px

def make_coloured_graph(G, communities):
    palette = itertools.cycle([f'rgb{tuple((np.array(color)*255).astype(np.uint8))}' for color in sns.color_palette(None, len(communities))])
    no_community = 'white'
    color_map = {}
    for cluster in communities:
        color = next(palette)
        for node in cluster:
            color_map[node] = color
    

import networkx as nx
from .database.DatabaseOG import Database, Data
from .clique_perc import Clique_Percolation, find_intensity
from .evolalgo import Chromosome, evolAlgo

class Cluster:
    def __init__(self, species, PPIDb):
        self.PPIDb = PPIDb
        self.species = species
        self.query = self.PPIDb.get_interactions_by_species(self.species)
        self.Interaction_Network = self.PPIDb.get_graph(self.query)
        self.clusters = {}
        self.cluster_nodes = {}
   
    def clusterFromPerc(self, k = 4, I = 0.05):
        self.clusters['cliqueperc'] = Clique_Percolation(self.Interaction_Network, k, I)
        

    def clusterFromGen(self, data, source):
        self.clusters[source] = []
        for i in self.query:
            for j in data:
                clusterobj = nx.Graph()
                for k in j:
                    for l in j:
                        if i['Gene A'] == k and i['Gene B'] == l or i['Gene B'] == l and i['Gene A'] == k:
                            clusterobj.add_edge(k, l)
                self.clusters[source].append(clusterobj)

    def get_clusterCount(self, source = 'all'):
        if source == 'all':
            return len(self.getClusters())
        elif source == 'cliqueperc' or source == 'genalgo':
            return len(self.get_clusters(source))

    def getClusters(self, source = 'all'):
        if source == 'all':
            return self.clusters['cliqeperc'] + self.clusters['genalgo']
        elif source == 'cliqueperc' or source == 'genalgo':
            return self.clusters[source]
    
    def get_cluster_size(self, source = 'all'):
        if source == 'all':
            return [len(i) for i in self.get_clusters()]
        elif source == 'cliqueperc' or source == 'genalgo':
            return [len(i) for i in self.get_clusters(source)]
            
    def get_network(self):
        return self.Interaction_Network
    

if __name__ == "__main__":
    PPIDb = Database()
    # print("init database")

    # query = PPIDb.get_interactions_by_species("Myxococcus xanthus")
    query = PPIDb.get_interactions_by_species("Treponema denticola")
    G = PPIDb.get_graph(query)
    communities = Clique_Percolation(G, 4, 0.05)
    print(communities)
    # clique = ['Q1CWQ1', 'ASGD', 'Q1D1W0', 'Q1CZP2']
    # print(G['Q1CWQ1']['ASGD']['weight'])
    # colours = [f'rgb{tuple((np.array(color)*255).astype(np.uint8))}' for color in sns.color_palette(None, 100)]
    # colours = px.colors.qualitative.Light24 + px.colors.qualitative.Pastel + px.colors.qualitative.Set3
    # colours += px.colors.qualitative.Set2
    # print(colours)
    # print(type(colours))
    # net = Network(notebook=True, bgcolor="#222222", font_color="white", height="100%", width="100%")
    # net.from_nx(graph)
    # net.show("PPIN.html")
    