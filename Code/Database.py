import pymongo
import urllib.parse
import urllib.request
import requests
import Data
import json

class Data: 
    def __init__(self) -> None:
        self.inter_data = {
            "Source" : "",
            "Database ID" : "", #the id of the interaction in the database source for the interaction
            "Gene A" : "", #the official symbol A for protein A
            "Gene B" : "", #the official symbol A for protein B
            "MINT Score" : "", #MINT score for the interaction
            "Type of data" : "", #primary or secondary data (produced by our algo)
            "Predicted Score" : "", #predicted score for interaction produced by our algo (is "-" if primary)
            "Experiment ID" : "" #_id in the experiment table for the interaction
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
    
    def get_inters(self):
        return self.inter_data 
    
    def get_proteins(self):
        return self.protein_data
    
    def get_taxons(self):
        return self.taxon_data
    
    def get_exps(self):
        return self.exp_data   
    
    def set_inters(self, source, db_id, GeneA, GeneB, score, type, pred_score, exp_id):
        self.inter_data["Source"] = source
        self.inter_data["Database ID"] = db_id
        self.inter_data["Gene A"] = GeneA
        self.inter_data["Gene B"] = GeneB
        self.inter_data["MINT Score"] = score
        self.inter_data["Type of data"] = type
        self.inter_data["Predicted Score"] = pred_score
        self.inter_data["Experiment ID"] = exp_id
        
        
    def set_proteins(self, gene, uniprotKB, taxon, desc):
        self.protein_data["_id"] = gene
        self.protein_data["Gene"] = gene
        self.protein_data["UniprotKB AC"] = uniprotKB
        self.protein_data["Taxon ID"] = taxon
        self.protein_data["Description"] = desc
    
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
        print("started client")
        self.ppiDB = self.clientDB["PPIdb"]
        print("init DB")
        self.interactions = self.ppiDB["interactions"]
        print("init interactions")
        self.proteins = self.ppiDB["proteins"]
        print("init proteins")
        self.taxonomy = self.ppiDB["taxonomy"]
        print("init taxon")
        self.expdetails = self.ppiDB["exp-details"]
        print("init exp details")

        print("Database connected")

    def insert_interaction(self, interaction, primary = True, geneA = "", geneB = "", score = ""):
        """Inserts an interaction object into the database"""
        if primary:
            try:
                self.interactions.insert_one(interaction)
            except:
                print("interaction already present")
    
    def insert_protein(self, protien):
        """Inserts a protien object into the database"""
        try:
            self.proteins.insert_one(protien)
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

    def remove_all_interactions(self, primary = True):
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
                
    def remove_protien(self, protien):
        for i in self.get_protiens():
            if protien == i:
                self.proteins.delete_one(i)

    def get_interactions(self, primary = True):
        if primary:
            return self.interactions.find()

    def get_protiens(self):
        return self.proteins.find()

    def get_interactions_by_protien(self, protien):
        return self.interactions.find({"Gene A" : protien}, {"Gene B" : protien})

    def get_interactions_by_type(self, type):
        return self.interactions.find({"Type of Data" : type})

    def get_interactions_by_score(self, score):
        return self.interactions.find({"MINT Score" : score})
    
    def get_interactions_by_database(self, database_name):
        return self.interactions.find({"Source" : database_name})
    
    def get_interactions_by_species(self, species_name):
        taxon_id = self.taxonomy.find_one({"Species Name" : species_name})["Taxon ID"]
        proteins = self.proteins.find({"Taxon ID" : taxon_id})
        interactions = []
        for protein in proteins:
            interactions.append(self.get_interactions_by_protien(protein))
        return interactions
        

    def get_all_prots(self):
        """Returns a list of nodes in the graph"""
        return self.proteins.find()
    
    def remove_everything(self):
        self.remove_all_expdet()        
        self.remove_all_interactions()
        self.remove_all_interactions(False)
        self.remove_all_proteins()
        self.remove_all_taxons()
        
    def get_stats(self):
        print("Number of primary interactions: " + str(self.interactions.count_documents({})))
        print("Number of protiens: " + str(self.proteins.count_documents({})))
        print("Number of taxons: " + str(self.taxonomy.count_documents({})))
        print("Number of exp details: " + str(self.expdetails.count_documents({})))

def get_species_name(gene, species):
    string_api_url = "https://version-11-5.string-db.org/api"
    output_format = "tsv-no-header"
    method = "get_string_ids"

    params = {
        "identifiers" : gene, # your protein list
        "species" : species, # species NCBI identifier 
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

def add_biogrid_data(file_name, db):
    file = open(file_name, 'r')
    file.readline()
    n = 1
    for line in file.readlines():
        data = Data()
        temp = line.split("\t")
        data.set_proteins(temp[7], get_uniprot_id(temp[7]), temp[15], "")
        db.insert_protein(data.get_proteins())
        print("added protein A :", data.get_proteins())
        data.set_proteins(temp[8], get_uniprot_id(temp[8]), temp[16], "")
        db.insert_protein(data.get_proteins())
        print("added protein B :", data.get_proteins())
        data.set_taxons(temp[15], temp[35])
        db.insert_taxon(data.get_taxons())
        print("added taxon A :", data.get_taxons())
        if temp[15] != temp[16]:
            data.set_taxons(temp[16], temp[36])
            db.insert_taxon(data.get_taxons())
            print("added taxon B :", data.get_taxons())
        data.set_exps(temp[11], temp[12], temp[13], temp[14])
        db.insert_expdet(data.get_exps())
        print("added exp details :", data.get_exps())
        data.set_inters(temp[22], temp[0], temp[7], temp[8], "", "Primary", "", data.get_exps()["_id"])
        db.insert_interaction(data.get_inters())
        print("added interaction :", data.get_inters())
        print("\n\n")
        n += 1
        if n == 6:
            break

def add_mint_data(file_name, db):
    file = open(file_name, 'r')
    file.readline()
    n = 1
    for line in file.readlines():
        data = Data()
        #Protein A;Gene A;Taxon A;Protein B;Gene B;Taxon B;Score;PMID
        temp = line.split(";")
        data.set_proteins(temp[1], get_uniprot_id(temp[1]), temp[2], "")
        db.insert_protein(data.get_proteins())
        print("added protein A")
        data.set_proteins(temp[4], get_uniprot_id(temp[4]), temp[5], "")
        db.insert_protein(data.get_proteins())
        print("added protein B")
        data.set_taxons(temp[2], get_species_name(temp[1], int(temp[2])))
        db.insert_taxon(data.get_taxons())
        print("added taxon A")
        if temp[15] != temp[16]:
            data.set_taxons(temp[5], get_species_name(temp[4], int(temp[5])))
            db.insert_taxon(data.get_taxons())
            print("added taxon B")
        data.set_exps("", "", "", temp[7])
        db.insert_expdet(data.get_exps())
        print("added exp details")
        data.set_inters("MINT", "", temp[1], temp[4], float(temp[6]), "Primary", "", data.get_exps()["_id"])
        db.insert_interaction(data.get_inters())
        print("added interaction")
        print("\n\n")
        n += 1
        if n == 6:
            break


def add_mentha_data(file_name, db, species):
    file = open(file_name, 'r')
    file.readline()
    taxon = 0
    if species == "Human":
        taxon = 9606
    n = 1
    for line in file.readlines():
        data = Data()
        #Protein A;Gene A;Protein B;Gene B;Score;mis
        temp = line.split(";")
        data.set_proteins(temp[1], get_uniprot_id(temp[1]), taxon, "")
        db.insert_protein(data.get_proteins())
        print("added protein A")
        data.set_proteins(temp[3], get_uniprot_id(temp[3]), taxon, "")
        db.insert_protein(data.get_proteins())
        print("added protein B")
        data.set_taxons(taxon, get_species_name(temp[1], taxon))
        db.insert_taxon(data.get_taxons())
        print("added taxon A")
        if temp[15] != temp[16]:
            data.set_taxons(taxon, get_species_name(temp[3], taxon))
            db.insert_taxon(data.get_taxons())
            print("added taxon B")
        data.set_exps("", "", "", "")
        db.insert_expdet(data.get_exps())
        print("added exp details")
        data.set_inters("Mentha", "", temp[1], temp[3], float(temp[5]), "Primary", "", data.get_exps()["_id"])
        db.insert_interaction(data.get_inters())
        print("added interaction")
        print("\n\n")
        n += 1
        if n == 6:
            break

# def add_string_data(file_name, db):
#     data = Data()

if __name__ == "__main__":
    Biogrid_db_addr = "D:\\Kaavish\\tempdata\\Biogrid-all-int.tsv"
    MINT_db_addr = "D:\\Kaavish\\tempData\\MINT-all-int.txt"
    Mentha_db_addr = "D:\\Kaavish\\tempData\\mentha-human-int.txt"
    PPIDb = Database()
    print("init database")
    
    add_biogrid_data(Biogrid_db_addr, PPIDb)
    add_mint_data(MINT_db_addr, PPIDb)
    add_mentha_data(Mentha_db_addr, PPIDb)
    
    # PPIDb.remove_everything()
    # print("removed everything")
    
    PPIDb.get_stats()
    print("got stats")

    # with open("Datasets/DONTEDIT/ppidb.json", "r") as read_file:
    #     data = json.load(read_file)
    # count = 0
    # for i in data["interactions"]:
    #     PPIDb.insert_interaction(data["interactions"][str(i)])
    #     count += 1
    #     if count == 5:
    #         break   
    #     # if count == 20:
    #     #     break
