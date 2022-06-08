import pymongo
import urllib.parse
import urllib.request
import requests
import time
from Bio import Entrez
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import json
from matplotlib.font_manager import json_load
from pyvis.network import Network


class Data:
    def __init__(self) -> None:

        self.inter_data = {
            "_id": "",
            "Source": "",
            "Database ID": "",  # the id of the interaction in the database source for the interaction
            "Gene A": "",  # the official symbol A for protein A
            "Gene B": "",  # the official symbol A for protein B
            "MINT Score": "",  # MINT score for the interaction
            "Experiment ID": ""  # _id in the experiment table for the interaction
        }

        self.protein_data = {
            "_id": "",
            "Gene": "",
            "UniprotKB AC": "",
            "Taxon ID": "",
            "Description": "",
            "ProtLen": "",
            "ProtWeight": "",
            "ClusterCof": "",
            "NumNeightbors": "",
            "UniquePep": "",
            "VarCount": "",
            "ProtAffinity": ""
        }

        self.taxon_data = {
            "_id": "",
            "Species Name": ""
        }

        self.exp_data = {
            "_id": "",
            "Experimental System": "",
            "Experiment System Type": "",
            "Author": "",
            "Publication Source (PubMed ID)": ""
        }

    def get_inters(self):
        return self.inter_data

    def get_proteins(self):
        return self.protein_data

    def get_taxons(self):
        return self.taxon_data

    def get_exps(self):
        return self.exp_data

    def set_inters(self, source, GeneA, GeneB, score, type_, exp_id):
        self.inter_data["_id"] = GeneA+"_"+GeneB
        self.inter_data["Source"] = source
        self.inter_data["Gene A"] = GeneA
        self.inter_data["Gene B"] = GeneB
        self.inter_data["MINT Score"] = score
        self.inter_data["Type of data"] = type_
        self.inter_data["Experiment ID"] = exp_id

    def set_proteins(self, gene, uniprotKB, taxon, protlen, protweight, clustercof, numneighbors, uniquepep, varcount, protAf):
        self.protein_data["_id"] = gene
        self.protein_data["UniprotKB AC"] = uniprotKB
        self.protein_data["Taxon ID"] = taxon
        self.protein_data["ProtLen"] = protlen
        self.protein_data["ProtWeight"] = protweight
        self.protein_data["ClusterCof"] = clustercof
        self.protein_data["NumNeightbors"] = numneighbors
        self.protein_data["UniquePep"] = uniquepep
        self.protein_data["VarCount"] = varcount
        self.protein_data["ProtAffinity"] = protAf

    def set_taxons(self, taxon, species):
        self.taxon_data["_id"] = taxon
        self.taxon_data["Species Name"] = species

    def set_exps(self, sys, sys_type, author, pubmed):
        self.exp_data["_id"] = pubmed


class Database:

    def __init__(self) -> None:
        self.clientDB = pymongo.MongoClient(
            "mongodb+srv://user:qwerty321@ppidb.3pazw.mongodb.net/PPIdb?retryWrites=true&w=majority")
        self.ppiDB = self.clientDB["PPIdb"]
        self.interactions = self.ppiDB["interactions"]
        self.proteins = self.ppiDB["proteins"]
        self.taxonomy = self.ppiDB["taxonomy"]
        self.expdetails = self.ppiDB["exp-details"]
        self.clusters = self.ppiDB["cluster"]

        print("Database connection initialiazed")

    # DB editors
    def insert_clusters(self, cluster_json):
        """Inserts a list of cluster objects into the database"""
        self.clusters.insert_many(cluster_json)
        
    def remove_all_clusters(self):
        self.clusters.delete_many({})
        
    def insert_interaction_list(self, interaction_json):
        """Inserts a list of interaction objects into the database"""
        self.interactions.insert_many(interaction_json, ordered = False)
        
    def insert_protein_list(self, protein_json):
        """Inserts a list of protein objects into the database"""
        self.proteins.insert_many(protein_json, ordered=False)
        
    def insert_taxon_list(self, taxonomy_json):
        """Inserts a list of taxonomy objects into the database"""
        self.taxonomy.insert_many(taxonomy_json)
        
    def insert_exp_detail_list(self, exp_json):
        """Inserts a list of exp_details objects into the database"""
        self.expdetails.insert_many(exp_json)
    
    def insert_interaction(self, interaction, primary=True, geneA="", geneB="", score=""):
        """Inserts an interaction object into the database"""
        if primary:
            try:
                self.interactions.insert_one(interaction)
            except:
                print("interaction already present")

    def insert_protein(self, protein):
        """Inserts a protein object into the database"""
        try:
            self.proteins.insert_one(protein)
        except:
            print("protein already present")

    def insert_taxon(self, taxon):
        """Inserts a taxonomy object into the database"""
        try:
            self.taxonomy.insert_one(taxon)
        except:
            print("taxon already present")

    def insert_expdet(self, expdet):
        """Inserts a experiment detail object into the database"""
        try:
            self.expdetails.insert_one(expdet)
        except:
            print("exp already present")

    def remove_all_interactions(self, primary=True):
        if primary:
            self.interactions.delete_many({})

    def remove_all_taxons(self):
        self.taxonomy.delete_many({})

    def remove_all_expdet(self):
        self.expdetails.delete_many({})

    def remove_all_proteins(self):
        self.proteins.delete_many({})

    def remove_interaction(self, interaction):
        for i in self.get_interactions():
            if interaction == i:
                self.interactions.delete_one(i)

    def remove_sec_interaction(self, interaction):
        for i in self.get_interactions(False):
            if interaction == i:
                self.sec_interactions.delete_one(i)

    def remove_protein(self, protein):
        for i in self.get_proteins():
            if protein == i:
                self.proteins.delete_one(i)

    def remove_everything(self):
        self.remove_all_expdet()
        self.remove_all_interactions()
        self.remove_all_interactions(False)
        self.remove_all_proteins()
        self.remove_all_taxons()

    def get_interactions(self, primary=True):
        if primary:
            return self.interactions.find()

    # DB getters
    def get_proteins(self):
        return self.proteins.find()

    def get_interactions_by_protein(self, protein):
        if isinstance(protein, str):
            return list(self.interactions.find({'$or': [
                {"Gene A": protein},
                {"Gene B": protein}
            ]}))
        else:
            return list(self.interactions.find({
                "Gene A": {"$in": protein},
            })) + list(self.interactions.find({
                "Gene B": {"$in": protein},
            }))

    def is_interaction_exist(self, proteinA, proteinB):
        ls = list(self.interactions.find({'$and': [
            {"Gene A": proteinA},
            {"Gene B": proteinB}
        ]})) + list(self.interactions.find({'$and': [
            {"Gene A": proteinB},
            {"Gene B": proteinA}
        ]}))
        return len(ls) > 0
    
    def get_interactions_by_type(self, type='Primary'):
        return list(self.interactions.find({"Type of data": type}))

    def get_interactions_by_score(self, score):
        return list(self.interactions.find({"MINT Score": score}))

    def get_interactions_by_database(self, database_name):
        return list(self.interactions.find({"Source": database_name}))

    def get_interactions_by_species(self, species_name):
        taxon_id = self.taxonomy.find_one(
            {"Species Name": species_name})["_id"]
        prim_proteins = self.proteins.find({"Taxon ID": taxon_id})

        interactions = []
        for protein in prim_proteins:
            # print('Protein Gene Name:', protein['Gene'])
            interactions += self.get_interactions_by_protein(protein['_id'])
        return self.get_complete_network(interactions)

    def get_all_prots(self, limit=-1):
        """Returns a list of nodes in the graph"""
        if limit == -1:
            return self.proteins.find()
        else:
            return self.proteins.find(limit=limit)
        
    def get_all_taxons(self, limit = -1):
        if limit == -1:
            return self.taxonomy.find()
        else:
            return self.taxonomy.find(limit=limit)

    def get_stats(self):
        print("Number of primary interactions: " +
              str(self.interactions.count_documents({})))
        print("Number of proteins: " + str(self.proteins.count_documents({})))
        print("Number of taxons: " + str(self.taxonomy.count_documents({})))
        print("Number of exp details: " +
              str(self.expdetails.count_documents({})))

    def get_graph(self, interactions):
        G = nx.Graph()
        for i in interactions:
            G.add_edge(i['Gene A'], i['Gene B'], weight=i['MINT Score'])
        return G

    def get_unweighted_graph(self, interactions) -> nx.Graph:
        G = nx.Graph()
        for i in interactions:
            G.add_edge(i['Gene A'], i['Gene B'])

    def get_adj_matrix(self, interactions):
        G = self.get_graph(interactions)
        return nx.to_numpy_matrix(G), G.nodes()

    def get_complete_network(self, query):
        proteins = {}
        for inter in query:
            proteins[inter['Gene A']] = None
            proteins[inter['Gene B']] = None
        return self.get_interactions_by_protein(list(proteins.keys()))

    def get_prot_features(self, prot):
        return self.get_affinity(prot), self.get_num_variations(prot), self.get_sequence_length(prot), self.get_loc_clustCof(prot)

    def get_affinity(self, protein, cutoff=1000):
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

    def get_num_variations(self, protein):
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

    def get_loc_clustCof(self, protein):

        nodes = self.get_interactions_by_protein(protein)
        nodelist = []
        # nodelist = [nodes[0] for n in nodes if nodes[0] != protein else nodes[1]]
        
        for n in nodes:
            if nodes[0] != protein:
                nodelist.append(nodes[0])
            else:
                nodelist.append(nodes[1])
        nodes = nodelist
        numNodes = len(nodes)
        numNeigborEdges = 0

        for i in nodes:
            for j in nodes:
                if i == j:
                    continue
                if self.is_interaction_exist(i, j) == True:
                    numNeigborEdges += 1

        return 2*numNeigborEdges/numNodes*(numNodes-1)

    def get_sequence_length(self, protein):
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
            seq += len(i["sequence"])
        return round(seq_len/count, 2)


def get_species_name(species):
    Entrez.email = 'prions.kaavish@gmail.com'  # Put your email here
    handle = Entrez.efetch('taxonomy', id=species, rettype='xml')
    response = Entrez.read(handle)
    taxonName = response[0].get('ScientificName')
    return taxonName


def get_uniprot_id(gene):
    url = 'https://www.uniprot.org/uploadlists/'

    params = {
        'from': 'GENENAME',
        'to': 'ACC',
        'format': 'tab',
        'query': gene
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
            'query': gene
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


def add_biogrid_data(file_name, db):
    file = open(file_name, 'r')
    file.readline()
    n = 1
    done = 400
    for line in file.readlines():
        print(n)
        if n < done:
            pass
        else:
            data = Data()
            temp = line.split("\t")
            data.set_proteins(temp[7], get_uniprot_id(temp[7]), temp[15], "")
            db.insert_protein(data.get_proteins())
            # print("added protein A :", data.get_proteins())
            data.set_proteins(temp[8], get_uniprot_id(temp[8]), temp[16], "")
            db.insert_protein(data.get_proteins())
            # print("added protein B :", data.get_proteins())
            data.set_taxons(temp[15], temp[35])
            db.insert_taxon(data.get_taxons())
            # print("added taxon A :", data.get_taxons())
            if temp[15] != temp[16]:
                data.set_taxons(temp[16], temp[36])
                db.insert_taxon(data.get_taxons())
                # print("added taxon B :", data.get_taxons())
            data.set_exps(temp[11], temp[12], temp[13], temp[14])
            db.insert_expdet(data.get_exps())
            # print("added exp details :", data.get_exps())
            data.set_inters(temp[22], temp[0], temp[7], temp[8],
                            "", "Primary", "", data.get_exps()["_id"])
            db.insert_interaction(data.get_inters())
            # print("added interaction :", data.get_inters())
            # print("\n\n")
        n += 1


def add_mint_data(file_name, db):
    file = open(file_name, 'r')
    file.readline()
    n = 1
    done = 1079
    for line in file.readlines():
        print(n)
        if n < done:
            pass
        else:
            data = Data()
            # print(line)
            # Protein A;Gene A;Taxon A;Protein B;Gene B;Taxon B;Score;PMID
            temp = line.split(";")
            temp[7] = temp[7].replace(" \n", "")
            data.set_proteins(temp[1], get_uniprot_id(temp[1]), temp[2], "")
            db.insert_protein(data.get_proteins())
            # print("added protein A :", data.get_proteins())
            data.set_proteins(temp[4], get_uniprot_id(temp[4]), temp[5], "")
            db.insert_protein(data.get_proteins())
            # print("added protein B :", data.get_proteins())
            data.set_taxons(temp[2], get_species_name(int(temp[2])))
            db.insert_taxon(data.get_taxons())
            # print("added taxon A :", data.get_taxons())
            if temp[2] != temp[5]:
                data.set_taxons(temp[5], get_species_name(int(temp[5])))
                db.insert_taxon(data.get_taxons())
                # print("added taxon B :", data.get_taxons())
            data.set_exps("", "", "", temp[7])
            db.insert_expdet(data.get_exps())
            # print("added exp details :", data.get_exps())
            data.set_inters("MINT", "", temp[1], temp[4], float(
                temp[6]), "Primary", "", data.get_exps()["_id"])
            db.insert_interaction(data.get_inters())
            # print("added interaction :", data.get_inters())
            print("\n\n")
        n += 1


def add_mentha_data(file_name, db, species):
    file = open(file_name, 'r')
    file.readline()
    taxon = 0
    if species == "Human":
        taxon = 9606
    n = 1
    for line in file.readlines():
        data = Data()
        # Protein A;Gene A;Protein B;Gene B;Score;mis
        temp = line.split(";")
        data.set_proteins(temp[1], get_uniprot_id(temp[1]), taxon, "")
        db.insert_protein(data.get_proteins())
        # print("added protein A")
        data.set_proteins(temp[3], get_uniprot_id(temp[3]), taxon, "")
        db.insert_protein(data.get_proteins())
        # print("added protein B")
        data.set_taxons(taxon, get_species_name(taxon))
        db.insert_taxon(data.get_taxons())
        # print("added taxon A")
        if temp[15] != temp[16]:
            data.set_taxons(taxon, get_species_name(taxon))
            db.insert_taxon(data.get_taxons())
            # print("added taxon B")
        data.set_exps("", "", "", "")
        db.insert_expdet(data.get_exps())
        # print("added exp details")
        data.set_inters("Mentha", "", temp[1], temp[3], float(
            temp[5]), "Primary", "", data.get_exps()["_id"])
        db.insert_interaction(data.get_inters())
        # print("added interaction")
        # print("\n\n")
        n += 1
        if n == 6:
            break


if __name__ == "__main__":
    # start = time.time()
    # Biogrid_db_addr = 'D:/Kaavish/tempData/Biogrid-all-int.txt'
    # MINT_db_addr = "D:/Kaavish/tempData/MINT-all-int.txt"
    # Mentha_db_addr = "D:/Kaavish/tempData/mentha-human-int.txt"
    # complex_addr = './allComplexes.json'
    PPIDb = Database()
    print("init database")
    
    # complexes = json_load(complex_addr)
    # PPIDb.insert_clusters(complexes)
    # print('Done')
    print([x['Species Name'] for x in list(PPIDb.get_all_taxons(5))])
    # add_biogrid_data(Biogrid_db_addr, PPIDb)
    # add_mint_data(MINT_db_addr, PPIDb)
    # add_mentha_data(Mentha_db_addr, PPIDb)

    # PPIDb.remove_all_expdet()
    # PPIDb.remove_all_interactions()
    # PPIDb.remove_all_interactions(False)
    # PPIDb.remove_everything()
    # print("removed everything")

    # PPIDb.get_stats()
    # print("got stats")

#     # for prot in PPIDb.get_all_prots(5):
#     #     print(prot)

#     # print(PPIDb.get_interactions_by_species("Caenorhabditis elegans"))

    # query = PPIDb.get_interactions_by_species("Myxococcus xanthus")
    # # query = PPIDb.get_interactions_by_protein(['SGK-1', 'DAF-16'])
    # graph = PPIDb.get_graph(query)
    # net = Network(notebook=True, bgcolor="#222222", font_color="white", height="100%", width="100%")
    # net.from_nx(graph)
    # net.show("PPIN.html")
#     print(PPIDb.get_adj_matrix(query))