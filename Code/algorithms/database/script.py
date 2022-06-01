from itertools import count
from urllib.error import HTTPError
from DatabaseOG import Database, Data
import urllib.parse
import urllib.request
import requests
import json
import time

import requests, sys

def get_affinity(protein, cutoff = 1000):
    """
    Get the affinity for a protein.
    """
    requestURL = "http://www.bindingdb.org/axis2/services/BDBService/getLigandsByUniprots?uniprot={0}&cutoff={1}&code=0&response=application/json".format(protein, cutoff)
    response = requests.get(requestURL)
    if not response.ok:
        return 0
    
    responseBody = response.json()
    affinity = 0
    responseBody = responseBody["getLigandsByUniprotsResponse"]["affinities"]
    print(responseBody)
    
    # affinity = sum(float(q['affinity']) for q in responseBody)
    
    affinity = 0
    count = 0
    for i in responseBody:
        try:
            affinity += i["affinity"]
            count += 1
        except TypeError:
            pass
    return round(affinity/count, 2)

def get_num_variations(protein):
    """
    Get the number of variations for a protein.
    """
    requestURL = "https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&gene={0}&categories=VARIANTS".format(protein)

    r = requests.get(requestURL, headers={ "Accept" : "application/json"})

    if not r.ok:
        # r.raise_for_status()
        return 1
    responseBody = r.json()
    return len(responseBody)
   
def get_loc_clustCof(db: Database, protein):

    nodes = db.get_interactions_by_protein(protein)
    nodes = [nodes[0] for n in nodes if nodes[0] != protein else nodes[1]]
    
    numNodes = len(nodes)
    numNeigborEdges = 0

    for i in nodes:
        for j in nodes: 
            if i == j:
                continue
            if db.is_interaction_exist((i,j)) == True:
                numNeigborEdges += 1

    return 2*numNeigborEdges/numNodes*(numNodes-1)

def get_sequence_length(protein):
    """
    Get the avg sequence length for a protein.
    """
    requestURL = "https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&gene={0}&categories=TOPOLOGY".format(protein)
    r = requests.get(requestURL, headers={ "Accept" : "application/json"})

    if not r.ok:
        # r.raise_for_status()
        return 1
    responseBody = r.json()
    seq_len = 0
    count = 0
    for i in responseBody:
        seq += len(i["sequence"])
    return round(seq_len/count, 2)


    
>>>>>>> 655cd7e983e4c81b7df220cddf75e895f7d59541
if __name__ == "__main__":
    # PPIDb = Database()
    # n = 0
    # for protein in PPIDb.get_proteins():
    #     gene = protein['UniprotKB AC']
    #     try:
    #         print(get_affinity(gene))
    #     except HTTPError:
    #         print("Error with", gene)
    #     n += 1
    #     if n == 11:
    #         break
        # print(protein)
        # PPIDb.update_affinity(protein, get_affinity(protein))
        # PPIDb.update_num_variations(protein, get_num_variations(protein))
        # time.sleep(1)
    # protein = 'P35355'
    protein_test = 'P45985'
    # # protein2 = 'RABGEF1'
    # protein3 = 'Q9UJ41'
    print(get_affinity(protein_test))
    # time.sleep(1)
    # # print(get_affinity(protein2))
    # # time.sleep(1)
    # print(get_affinity(protein3))
    # # print(get_num_variations(protein2))
    