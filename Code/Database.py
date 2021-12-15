import pymongo
import urllib.parse
import urllib.request
import requests
import json

class Data: 
    def __init__(self) -> None:
        self.prim_inter_data = {
            "Source" : "",
            "Database ID" : "", #the id listed in the database source for the interaction
            "Gene A" : "", #the official symbol A for protein A
            "Gene B" : "", #the official symbol A for protein B
            "MINT Score" : "", #MINT score for the interaction
        }
        
        self.sec_inter_data = {
            "Source" : "",
            "Database ID" : "", #the id listed in the database source for the interaction
            "Gene A" : "", #the official symbol A for protein A
            "Gene B" : "", #the official symbol A for protein B
            "MINT Score" : "", #MINT score for the interaction
            "Predicted Score" : "" #score from ensemble
        }
        
        self.protein_data = {
            "_id" : "",
            "Gene" : "", 
            "UniprotKB AC" : "",
            "Taxon ID" : "",
            "Description" : ""
        }
        
        self.taxon_data = {
            "_id" : "",
            "Taxon ID" : "",
            "Species Name" : "" 
        }
        
        self.exp_data = {
            "Experimental System" : "",
            "Experiment System Type" : "",
            "Author" : "",
            "Publication Source (PubMed ID)" : ""
        }
    
    def get_prim_inters(self):
        return self.prim_inter_data 
    
    def get_sec_inters(self):
        return self.sec_inter_data
    
    def get_proteins(self):
        return self.protein_data
    
    def get_taxons(self):
        return self.taxon_data
    
    def get_exps(self):
        return self.exp_data   
    
    def set_prim_inters(self, source, db_id, taxonA, taxonB, score):
        self.prim_inter_data["Source"] = source
        self.prim_inter_data["Database ID"] = db_id
        self.prim_inter_data["Taxon ID A"] = taxonA
        self.prim_inter_data["Taxon ID B"] = taxonB
        self.prim_inter_data["MINT Score"] = score
        
    def set_sec_inters(self, source, db_id, taxonA, taxonB, score, pred_score):
        self.sec_inter_data["Source"] = source
        self.sec_inter_data["Database ID"] = db_id
        self.sec_inter_data["Taxon ID A"] = taxonA
        self.sec_inter_data["Taxon ID B"] = taxonB
        self.sec_inter_data["MINT Score"] = score
        self.sec_inter_data["Predicted Score"] = pred_score
        
    def set_proteins(self, gene, uniprotKB, taxon, desc):
        self.protein_data["_id"] = gene
        self.protein_data["Gene"] = gene
        self.protein_data["UniprotKB AC"] = uniprotKB
        self.protein_data["Taxon ID"] = taxon
        self.protein_data["Description""Gene"] = desc
    
    def set_taxons(self, taxon, species):
        self.taxon_data["_id"] = taxon
        self.taxon_data["Taxon ID"] = taxon
        self.taxon_data["Species Name"] = species
        
    def set_exps(self, sys, sys_type, author, pubmed):
        self.exp_data["Experimental System"] = sys
        self.exp_data["Experiment System Type"] = sys_type
        self.exp_data["Author"] = author
        self.exp_data["Publication Source (PubMed ID)"] = pubmed

        
class Database:

    def __init__(self) -> None:
        self.clientDB = pymongo.MongoClient("mongodb+srv://user:qwerty321@ppidb.3pazw.mongodb.net/PPIdb?retryWrites=true&w=majority")
        print("set client")
        self.ppiDB = self.clientDB["PPIdb"]
        print("selected db")
        self.prim_interactions = self.ppiDB["prim-interactions"]
        print("set primary interactions")
        self.sec_interactions = self.ppiDB["sec-interactions"]
        print("set secondary interactions")
        self.proteins = self.ppiDB["proteins"]
        print("set proteins")
        self.taxonomy = self.ppiDB["taxonomy"]
        print("set taxonomy")
        self.expdetails = self.ppiDB["exp-details"]
        print("set exp-details")

        # self.countPrimInteractions = self.prim_interactions.count_documents({})
        # self.countSecInteractions = self.sec_interactions.count_documents({})
        # self.countProtiens = self.proteins.count_documents({})

        print("Database connected")

    def insert_interaction(self, interaction, primary = True):
        """Inserts an interaction object into the database"""
        if primary:
            self.prim_interactions.insert_one(interaction)
        else:
            self.sec_interactions.insert_one(interaction)
    
    def insert_protein(self, protien):
        """Inserts a protien object into the database"""
        self.proteins.insert_one(protien)
        
    def insert_taxon(self, taxon):
        """Inserts a taxonomy object into the database"""
        self.taxonomy.insert_one(taxon)
        
    def insert_expdet(self, expdet):
        """Inserts a experiment detail object into the database"""
        self.expdetails.insert_one(expdet)

    def remove_all_interactions(self):
        self.prim_interactions.delete_many({})
    
    def remove_all_proteins(self):
        self.proteins.delete_many({})   
    
    def remove_prim_interaction(self, interaction):
        for i in self.get_interactions():
            if interaction == i:
                self.prim_interactions.delete_one(i) 
                 
    def remove_sec_interaction(self, interaction):
        for i in self.get_interactions(False):
            if interaction == i:
                self.sec_interactions.delete_one(i)  
                
    def remove_protien(self, protien):
        for i in self.get_protiens():
            if protien == i:
                self.proteins.delete_one(i)

    def get_interactions(self, primary = True):
        if primary:
            return self.prim_interactions.find()
        else:
            return self.sec_interactions.find()

    def get_protiens(self):
        return self.proteins.find()

    def get_interactions_by_protien(self, protien):
        pass

    def get_interactions_by_type(self, type):
        pass

    def get_interactions_by_score(self, score):
        pass

    def get_all_prots(self):
        """Returns a list of nodes in the graph"""
        return self.proteins.find()
        pass

    def get_stats(self):
        print("Number of primary interactions: " + str(self.countPrimInteractions))
        print("Number of secondary interactions: " + str(self.countSecInteractions))
        print("Number of protiens: " + str(self.countProtiens))

def get_species_name(gene):
    string_api_url = "https://version-11-5.string-db.org/api"
    output_format = "tsv-no-header"
    method = "get_string_ids"

    params = {

        "identifiers" : gene, # your protein list
        "species" : 9606, # species NCBI identifier 
        "limit" : 1, # only one (best) identifier per input protein
        "echo_query" : 1, # see your input identifiers in the output
        "caller_identity" : "www.awesome_app.org" # your app name

    }

    request_url = "/".join([string_api_url, output_format, method])
    results = requests.post(request_url, data=params)

    for line in results.text.strip().split("\n"):
        l = line.split("\t")
        taxonName = l[4]
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
    return (response.decode('utf-8').split("\n")[1].split("\t")[1])

def add_biogrid_data(file_name, db, all = True):
    data = Data()
    file = open(file_name, 'r')
    for line in file.readlines():
        temp = line.split("\t")
        data.set_prim_inters("Biogrid", temp[0], temp[7], temp[8], "")
        db.insert_interaction(data.get_prim_inters())
        print("added interaction")
        data.set_proteins(temp[7], get_uniprot_id(temp[7]), temp[15], "")
        db.insert_protein(data.get_proteins())
        print("added protein A")
        data.set_proteins(temp[8], get_uniprot_id(temp[8]), temp[16], "")
        db.insert_protein(data.get_proteins())
        print("added protein B")
        data.set_taxons(temp[15], get_species_name(temp[7]))
        db.insert_taxon(data.get_taxons())
        print("added taxon A")
        if temp[15] != temp[16]:
            data.set_taxons(temp[16], get_species_name(temp[8]))
            db.insert_taxon(data.get_taxons())
            print("added taxon B")
        data.set_exps(temp[11], temp[12], temp[13], temp[14])
        db.insert_expdet(data.get_exps())
        print("added exp details")
        print("\n\n")

# def add_mint_data(file_name, db):
#     data = Data()

# def add_string_data(file_name, db):
#     data = Data()

# def add_mentha_data(file_name, db):
#     data = Data()

if __name__ == "__main__":
    PPIDb = Database()
    print("init database")
    # add_biogrid_data("Biogrid-all-int.tsv", PPIDb)
    PPIDb.remove_all_interactions()
    PPIDb.remove_all_interactions(False)
    PPIDb.remove_all_proteins()
    PPIDb.get_stats()


    with open("Datasets/DONTEDIT/ppidb.json", "r") as read_file:
        data = json.load(read_file)
    count = 0
    for i in data["interactions"]:
        PPIDb.insert_interaction(data["interactions"][str(i)])
        count += 1
        if count == 10:
            break   
        # if count == 20:
        #     break
