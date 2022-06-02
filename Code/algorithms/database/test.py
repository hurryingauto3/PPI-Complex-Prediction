from itertools import count
from urllib.error import HTTPError
from itsdangerous import NoneAlgorithm
from DatabaseOG import Database, Data
import urllib.parse
import urllib.request
import requests
import json
import time
import pandas as pd
from Bio import Entrez
import requests, sys
import numpy as np

def get_uniprot_ids(genes, taxon = '9606'):
    url = 'https://www.uniprot.org/uploadlists/'

    params = {
        'from': 'GENENAME',
        'to': 'ACC',
        'format': 'tab',
        'query': genes,
        'taxon' : taxon
    }

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
    return response.decode('utf-8')

if __name__ == "__main__":
    genes = ['MTMR4', 'CRYBG3', 'ANKRD40', 'EHD3']
    gene_string = ' '.join(genes)
    print(get_uniprot_ids(gene_string))