import urllib.parse
import urllib.request
import requests

# import pymongo
# client = pymongo.MongoClient("mongodb+srv://user:qwerty321@ppidb.3pazw.mongodb.net/PPIdb?retryWrites=true&w=majority")
# db = client.test

# # file_loc = "Datasets\human-prot\string-all-prot.txt"
# # string_prot = open(file_loc, 'r')
# # print(string_prot.readline())

# #!/usr/bin/env python3

# ##########################################################
# ## For a given list of proteins the script resolves them
# ## (if possible) to the best matching STRING identifier
# ## and prints out the mapping on screen in the TSV format
# ##
# ## Requires requests module:
# ## type "python -m pip install requests" in command line
# ## (win) or terminal (mac/linux) to install the module
# ###########################################################

# import requests ## python -m pip install requests

# string_api_url = "https://version-11-5.string-db.org/api"
# output_format = "tsv-no-header"
# method = "get_string_ids"

# ##
# ## Set parameters
# ##

# params = {

#     "identifiers" : "BRCA1", # your protein list
#     "species" : 9606, # species NCBI identifier
#     "limit" : 1, # only one (best) identifier per input protein
#     "echo_query" : 1, # see your input identifiers in the output
#     "caller_identity" : "www.awesome_app.org" # your app name

# }

# ##
# ## Construct URL
# ##


# request_url = "/".join([string_api_url, output_format, method])

# ##
# ## Call STRING
# ##

# results = requests.post(request_url, data=params)

# ##
# ## Read and parse the results
# ##

# for line in results.text.strip().split("\n"):
#     l = line.split("\t")
#     input_identifier, taxonId, taxonName = l[0], l[3], l[4]
#     print("Input:", input_identifier, "Taxon ID:", taxonId,"Taxon:", taxonName, sep="\t")

# # import urllib.parse
# # import urllib.request

# # url = 'https://www.uniprot.org/uploadlists/'

# # params = {
# # 'from': 'GENENAME',
# # 'to': 'ACC',
# # 'format': 'tab',
# # 'query': 'MDH1'
# # }

# # data = urllib.parse.urlencode(params)
# # data = data.encode('utf-8')
# # req = urllib.request.Request(url, data)
# # with urllib.request.urlopen(req) as f:
# #    response = f.read()
# # print(response.decode('utf-8').split("\n")[1].split("\t")[1])

# file_name = "D:\\tempdata\\Biogrid-all-int.tsv"
# file = open(file_name, 'r')
# file.readline()
# n = 1
# for line in file.readlines():
#     temp = line.split("\t")
#     print(temp)
#     n += 1
#     if n == 6:
#         break

# import urllib.parse
# import urllib.request

# def get_uniprot_id(gene):
#     url = 'https://www.uniprot.org/uploadlists/'

#     params = {
#         'from': 'GENENAME',
#         'to': 'ACC',
#         'format': 'tab',
#         'query': gene
#     }

#     data = urllib.parse.urlencode(params)
#     data = data.encode('utf-8')
#     req = urllib.request.Request(url, data)
#     with urllib.request.urlopen(req) as f:
#         response = f.read()
#     return (response.decode('utf-8').split("\n")[1].split("\t")[1])

# gene = "BVLF1 {ECO:0000313|EMBL:CAJ75461.1}"
# gene = 'CRYBG3'
# print(get_uniprot_id(gene))


# def get_species_name(gene, species):
#     string_api_url = "https://version-11-5.string-db.org/api"
#     output_format = "tsv-no-header"
#     method = "get_string_ids"

#     params = {
#         "identifiers" : gene, # your protein list
#         "species" : species, # species NCBI identifier
#         "limit" : 1, # only one (best) identifier per input protein
#         "echo_query" : 1, # see your input identifiers in the output
#         "caller_identity" : "www.awesome_app.org" # your app name
#     }

#     request_url = "/".join([string_api_url, output_format, method])
#     results = requests.post(request_url, data=params)

#     print(results)
#     for line in results.text.strip().split("\n"):
#         l = line.split("\t")
#         taxonName = l[4]
#         return taxonName

# print(get_species_name("BVLF1 {ECO:0000313|EMBL:CAJ75461.1}", 10377))
# from Bio import Entrez
# tax_ids = [10377]
# Entrez.email = 'prions.kaavish@gmail.com'  # Put your email here
# handle = Entrez.efetch('taxonomy', id=tax_ids, rettype='xml')
# response = Entrez.read(handle)
# taxonName = response[0].get('ScientificName')
# print(taxonName)

# def get_uniprot_id(gene):
#     url = 'https://www.uniprot.org/uploadlists/'

#     params = {
#         'from': 'ACC+ID',
#         'to': 'GENENAME',
#         'format': 'tab',
#         'query': gene
#     }

#     data = urllib.parse.urlencode(params)
#     data = data.encode('utf-8')
#     req = urllib.request.Request(url, data)
#     with urllib.request.urlopen(req) as f:
#         response = f.read()
#     print(response.decode('utf-8'))
#     # return (response.decode('utf-8').split("\n")[1].split("\t")[1])


# get_uniprot_id("B4E2V5")
# # print(get_uniprot_id("P53235"))

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pylab
import time

sample_adj_list = {
    0: [1, 2, 3],
    1: [0, 2],
    2: [0, 1, 3],
    3: [0, 4, 5],
    4: [3, 5, 6, 7],
    5: [3, 4, 6, 7],
    6: [4, 5, 7, 8],
    7: [4, 5, 6],
    8: [6]
}

sample_adj_matrix = [
    #[1, 2, 3, 4, 5, 6, 7, 8, 9]
    [0, 2, 3, 4, 0, 0, 0, 0, 0],
    [2, 0, 4, 0, 0, 0, 0, 0, 0],
    [3, 4, 0, 5, 0, 0, 0, 0, 0],
    [4, 0, 5, 0, 6, 7, 0, 0, 0],
    [0, 0, 0, 6, 0, 8, 9, 3, 0],
    [0, 0, 0, 7, 8, 0, 2, 4, 0],
    [0, 0, 0, 0, 9, 2, 0, 5, 6],
    [0, 0, 0, 0, 3, 4, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 0],
]


def find_intensity(clique, G, k):
    prod = 1
    for i in range(len(clique)):
        for j in range(i+1, len(clique)):
            prod = prod * G[i][j]['weight']
    return prod**(2/(k*(k-1)))


def Clique_Percolation(adj_matrix, k, I):
    # start = time.time()
    G = nx.from_numpy_matrix(np.matrix(adj_matrix))
    # G = nx.Graph(adj_matrix)
    cliques = [clique for clique in nx.enumerate_all_cliques(
        G) if len(clique) == k]

    print(find_intensity(cliques[0], G, k))
    return cliques
    # clique_map = {}
    # for i in range(len(cliques)):
    #     if find_intensity(cliques[i], G, k) > I:
    #         clique_map[i+1] = cliques[i]
    # perculated_graph = nx.Graph()
    # perculated_graph.add_nodes_from(clique_map.keys())


print(Clique_Percolation(sample_adj_matrix, 3, 1))
