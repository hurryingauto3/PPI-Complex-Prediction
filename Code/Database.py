from os import error
import pymongo

class Database:

    def __init__(self) -> None:
        self.clientDB = pymongo.MongoClient("mongodb+srv://user:qwerty321@ppidb.3pazw.mongodb.net/PPIdb?retryWrites=true&w=majority")
        self.ppiDB = self.clientDB["PPIdb"]
        self.prim_interactions = self.ppiDB["prim-interactions"]
        self.sec_interactions = self.ppiDB["sec-interactions"]
        self.proteins = self.ppiDB["proteins"]
        self.taxonomy = self.ppiDB["taxonomy"]
        self.expdetails = self.ppiDB["exp-details"]
        # self.countPrimInteractions = self.prim_interactions.count_documents({})
        # self.countSecInteractions = self.sec_interactions.count_documents({})
        # self.countProtiens = self.proteins.count_documents({})

        print("Database connected")

    def insert_interaction(self, interaction, primary = True, geneA = "", geneB = "", score = ""):
        """Inserts an interaction object into the database"""
        if primary:
            try:
                self.prim_interactions.insert_one(interaction)
            except error as e:
                print(e)
        else:
            self.sec_interactions.insert_one(interaction)
    
    def insert_protein(self, protien):
        """Inserts a protien object into the database"""
        try:
            self.proteins.insert_one(protien)
        except error as e:
            print(e)
        
    def insert_taxon(self, taxon):
        """Inserts a taxonomy object into the database"""
        try:
            self.taxonomy.insert_one(taxon)
        except error as e:
            print(e)

    def insert_expdet(self, expdet):
        """Inserts a experiment detail object into the database"""
        try:
            self.expdetails.insert_one(expdet)
        except error as e:
            print(e)

    def remove_all_interactions(self, primary = True):
        if primary:
            self.prim_interactions.delete_many({})
        else:
            self.sec_interactions.delete_many({})
        
    def remove_all_taxons(self):
        self.taxonomy.delete_many({})
        
    def remove_all_expdet(self):
        self.expdetails.delete_many({})
        
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
    
    def remove_everything(self):
        self.remove_all_expdet()
        self.remove_all_interactions()
        self.remove_all_interactions(False)
        self.remove_all_proteins()
        self.remove_all_taxons()
        
    def get_stats(self):
        print("Number of primary interactions: " + str(self.prim_interactions.count_documents({})))
        print("Number of secondary interactions: " + str(self.sec_interactions.count_documents({})))
        print("Number of protiens: " + str(self.proteins.count_documents({})))
        print("Number of taxons: " + str(self.taxonomy.count_documents({})))
        print("Number of exp details: " + str(self.expdetails.count_documents({})))

