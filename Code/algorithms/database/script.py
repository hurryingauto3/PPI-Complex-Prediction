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

def get_species_name(species):
    Entrez.email = 'prions.kaavish@gmail.com'  # Put your email here
    handle = Entrez.efetch('taxonomy', id=species, rettype='xml')
    response = Entrez.read(handle)
    taxonName = response[0].get('ScientificName')
    return taxonName

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

def get_uniprot_id(gene, taxon = '9606'):
    url = 'https://www.uniprot.org/uploadlists/'

    params = {
        'from': 'GENENAME',
        'to': 'ACC',
        'format': 'tab',
        'query': gene,
        'taxon' : taxon
    }

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
    try:
        (response.decode('utf-8').split("\n")[1].split("\t")[1])
    except:
        params = {
            'from': 'ACC',
            'to': 'GENENAME',
            'format': 'tab',
            'query': gene,
            'taxon' : taxon
        }

        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as f:
            response = f.read()
        try:
            return (response.decode('utf-8').split("\n")[1].split("\t")[1])
        except:
            return "Unknown"

def get_affinity(protein, cutoff=1000):
    """
    Get the affinity for a protein.
    """
    requestURL = "http://www.bindingdb.org/axis2/services/BDBService/getLigandsByUniprots?uniprot={0}&cutoff={1}&code=0&response=application/json".format(
        protein, cutoff)
    response = requests.get(requestURL)
    if not response.ok:
        return 0

    responseBody = response.json()
    affinity = 0
    try:
        responseBody = responseBody["getLigandsByUniprotsResponse"]["affinities"]
    except:
        return 0
    print('got affinity')

    # affinity = sum(float(q['affinity']) for q in responseBody)

    affinity = 0
    count = 0
    for i in responseBody:
        try:
            affinity += i["affinity"]
            count += 1
        except TypeError:
            pass
    if count == 0:
        return 0
    return round(affinity/count, 2)

def get_num_variations(protein):
    """
    Get the number of variations for a protein.
    """
    requestURL = "https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&gene={0}&categories=VARIANTS".format(
        protein)

    r = requests.get(requestURL, headers={"Accept": "application/json"})

    if not r.ok:
        # r.raise_for_status()
        return 1
    responseBody = r.json()
    return len(responseBody)

def get_sequence_length(protein):
    """
    Get the avg sequence length for a protein.
    """
    requestURL = "https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&gene={0}&categories=TOPOLOGY".format(
        protein)
    r = requests.get(requestURL, headers={"Accept": "application/json"})

    if not r.ok:
        # r.raise_for_status()
        return 1
    responseBody = r.json()
    seq_len = 0
    count = 0
    for i in responseBody:
        try:
            seq_len += len(i["sequence"])
            count += 1
        except TypeError:
            pass
    if count == 0:
        return 0
    return round(seq_len/count, 2)


#Protein A;Gene A;Taxon A;Protein B;Gene B;Taxon B;Score;PMID
        
def add_mint_data_from_file(file_name, db):
    df = pd.read_csv(file_name, sep = ';')
    # df = df.head(5)
    taxonA = df['Taxon A'].unique()
    taxonB = df['Taxon B'].unique()
    taxons = np.concatenate((taxonA, taxonB), axis = None)
    taxons = np.unique(taxons)
    taxon_list = pd.DataFrame({'_id':taxons})
    print('getting species names')
    # taxon_list['Species Name'] = [get_species_name(x) for x in taxon_list['_id']]
    # taxon_json = json.loads(taxon_list.to_json(orient='table',index=False))
    # db.insert_taxon_list(taxon_json['data'])    
    proteins = None
    not_done = [210, 632, 882]
    for taxon in taxon_list['_id']:
        print('taxon =', taxon)
        if taxon > 882:
            proteinA = df[df['Taxon A'] == taxon].iloc[:, :3]
            proteinA = proteinA[['Gene A', 'Protein A', 'Taxon A']]
            proteinA.rename(columns = {'Protein A':'UniprotKB AC', 'Gene A':'_id', 'Taxon A':'Taxon ID'}, inplace = True)
            proteinB = df[df['Taxon B'] == taxon].iloc[:, 3:6]
            proteinB = proteinB[['Gene B', 'Protein B', 'Taxon B']]
            proteinB.rename(columns = {'Protein B':'UniprotKB AC', 'Gene B':'_id', 'Taxon B':'Taxon ID'}, inplace = True)
            protein_frame = [proteinA, proteinB]
            proteins = pd.concat(protein_frame)
            proteins = proteins.drop_duplicates()
            proteins['Affinity'] = [get_affinity(x) for x in proteins['UniprotKB AC']]
            proteins['Variations'] = [get_num_variations(x) for x in proteins['_id']]
            proteins['SeqLength'] = [get_sequence_length(x) for x in proteins['_id']]
            protein_json = json.loads(proteins.to_json(orient='table',index=False))
            try:
                db.insert_protein_list(protein_json['data'])
            except:
                not_done.append(taxon)
    # interactions = pd.DataFrame()
    # interactions['_id'] = df['Gene A'] + '_' + df['Gene B']
    # interactions['Gene A'] = df['Gene A']
    # interactions['Gene B'] = df['Gene B']
    # interactions['MINT Score'] = df['Score']
    # interactions['Source'] = 'MINT'
    # interactions['Experiment ID'] = df['PMID']
    # interaction_json = json.loads(interactions.to_json(orient='table',index=False))
    # db.insert_interaction_list(interaction_json['data'])
    # print(interactions)
    print(not_done)
    print('done')
    
    
    # 
    
        
   
if __name__ == "__main__":
    PPIDb = Database()
    Biogrid_db_addr = 'D:/Kaavish/tempData/Biogrid-all-int.txt'
    MINT_db_addr = "D:/Kaavish/tempData/MINT-all-int.txt"
    Mentha_db_addr = "D:/Kaavish/tempData/mentha-human-int.txt"
    # gene_list = ['MTMR4', 'CRYBG3', 'ANKRD40', 'EHD3', 'RAB8A', 'Q9NYA4', 'Q68DQ2', 'Q6AI12', 'Q9NZN3', 'P61006']
    # gene_list = ['Q9NYA4', 'Q68DQ2', 'Q6AI12', 'Q9NZN3', 'P61006']
    # for gene in gene_list:
    #     print(get_affinity(gene))
    add_mint_data_from_file(MINT_db_addr, PPIDb)
    # PPIDb.remove_everything()
    # df = pd.read_csv(MINT_db_addr,sep=';')
    
    
    # taxon_listB = df['Taxon B'].unique()
    
    # protein_test = 'P45985'
    