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
    

if __name__ == "__main__":
    # PPIDb = Database()
    # print("init database")

    # query = PPIDb.get_interactions_by_species("Myxococcus xanthus")
    # G = PPIDb.get_graph(query)
    # communities = Clique_Percolation(G, 4, 0.05)
    # print(communities)
    # clique = ['Q1CWQ1', 'ASGD', 'Q1D1W0', 'Q1CZP2']
    # print(G['Q1CWQ1']['ASGD']['weight'])
    colours = [f'rgb{tuple((np.array(color)*255).astype(np.uint8))}' for color in sns.color_palette(None, 100)]
    # colours = px.colors.qualitative.Light24 + px.colors.qualitative.Pastel + px.colors.qualitative.Set3
    # colours += px.colors.qualitative.Set2
    print(colours)
    print(type(colours))
    # net = Network(notebook=True, bgcolor="#222222", font_color="white", height="100%", width="100%")
    # net.from_nx(graph)
    # net.show("PPIN.html")
    