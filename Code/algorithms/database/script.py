from itertools import count
from urllib.error import HTTPError
from DatabaseOG import Database, Data
import urllib.parse
import urllib.request
import requests
import json
import time

import requests, sys


   
if __name__ == "__main__":
    PPIDb = Database()
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
    print(get_loc_clustCof(protein_test))
    # time.sleep(1)
    # # print(get_affinity(protein2))
    # # time.sleep(1)
    # print(get_affinity(protein3))
    # # print(get_num_variations(protein2))
    