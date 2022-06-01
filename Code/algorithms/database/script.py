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
        response.raise_for_status()
        sys.exit()
    
    responseBody = response.json()
    responseBody = responseBody["getLigandsByUniprotsResponse"]["affinities"]
    affinity = sum(float(q['affinity']) for q in responseBody)
    
    return affinity

def get_num_variations(protein):
    """
    Get the number of variations for a protein.
    """
    requestURL = "https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&gene={0}&categories=VARIANTS".format(protein)

    r = requests.get(requestURL, headers={ "Accept" : "application/json"})

    if not r.ok:
        # r.raise_for_status()
        sys.exit()
    responseBody = r.json()
    return len(responseBody)
   
if __name__ == "__main__":
    PPIDb = Database()
    n = 0
    for protein in PPIDb.get_proteins():
        gene = protein['UniprotKB AC']
        try:
            print(get_affinity(gene))
        except HTTPError:
            print("Error with", gene)
        n += 1
        if n == 11:
            break
        # print(protein)
        # PPIDb.update_affinity(protein, get_affinity(protein))
        # PPIDb.update_num_variations(protein, get_num_variations(protein))
        # time.sleep(1)
    # protein = 'P35355'
    # # protein2 = 'RABGEF1'
    # protein3 = 'Q9UJ41'
    # print(get_affinity(protein))
    # time.sleep(1)
    # # print(get_affinity(protein2))
    # # time.sleep(1)
    # print(get_affinity(protein3))
    # # print(get_num_variations(protein2))
    