import pymongo

class Database:

    def __init__(self) -> None:
        self.clientDB = pymongo.MongoClient("mongodb+srv://user:qwerty321@ppidb.3pazw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.ppiDB = self.clientDB["PPIdb"]
        self.priminteractions = self.ppiDB["prim-interactions"]
        self.secinteractions = self.ppiDB["sec-interactions"]
        self.proteins = self.ppiDB["proteins"]
        self.taxonomy = self.ppiDB["taxonomy"]
        self.expdetails = self.clientDB["exp-details"]

        self.countPrimInteractions = self.priminteractions.count_documents({})
        self.countSecInteractions = self.secinteractions.count_documents({})
        self.countProtiens = self.proteins.count_documents({})

        print("Database connected")

    def insert_interaction(self, interaction, primary = True):
        """Inserts an interaction object into the database"""
        if primary:
            self.priminteractions.insert_one(interaction)
        else:
            self.secinteractions.insert_one(interaction)
    
    def insert_protien(self, protien):
        """Inserts a protien object into the database"""
        self.proteins.insert_one(protien)

    def remove_all_interactions(self):
        self.priminteractions.delete_many({})
    
    def remove_all_protiens(self):
        self.proteins.delete_many({})   
    
    def remove_interaction(self, interaction):
        for i in self.get_interactions():
            if interaction == i:
                self.Interactions.delete_one(i)    
    def remove_protien(self, protien):
        for i in self.get_protiens():
            if protien == i:
                self.Protien.delete_one(i)

    def get_interactions(self, primary = True):
        if primary:
            return self.priminteractions.find()
        else:
            return self.secinteractions.find()

    def get_protien(self):
        return self.proteins.find()

    def get_interactions_by_protien(self, protien):
        pass

    def get_interactions_by_type(self, type):
        pass

    def get_interactions_by_score(self, score):
        pass

    def get_all_prots(self):
        """Returns a list of nodes in the graph"""
        return self.Protien.find()
        pass

    def get_stats(self):
        print("Number of primary interactions: " + str(self.countPrimInteractions))
        print("Number of secondary interactions: " + str(self.countSecInteractions))
        print("Number of protiens: " + str(self.countProtiens))
    
if __name__ == "__main__":
    PPIDB = Database()
    PPIDB.insert_interaction({"protien1": "MDH2", "protien2": "MDH3", "type": "primary"})
    PPIDB.insert_interaction({"protien1": "MDH2", "protien2": "MDH3", "type": "secondary"})

    print(PPIDB.get_interactions())