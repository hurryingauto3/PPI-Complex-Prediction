import pymongo

class Database:

    def __init__(self, port) -> None:
        self.clientDB = pymongo.MongoClient("mongodb://localhost:" + str(port) + "/")
        self.ppiDB = self.clientDB["PPIdb"]
        self.Interactions = self.ppiDB["Interactions"]
        self.Protien = self.ppiDB["Protien"]
        self.InteractionCount = self.ppiDB.Interactions.count_documents({})
        self.ProtienCount = self.ppiDB.Protien.count_documents({})
        print("Database connected")

    def insert_interaction(self, interaction):
        """Inserts an interaction object into the database"""
        self.ppiDB.Interactions.insert_one(interaction)
        self.update_stats("Interaction")
    
    def insert_protien(self, protien):
        """Inserts a protien object into the database"""
        self.ppiDB.Protien.insert_one(protien)
        self.update_stats("Protien")
    
    def remove_all_interactions(self):
        self.Interactions.delete_many({})
        self.update_stats("Interaction")
    
    def remove_all_protiens(self):
        self.Protien.delete_many({})
        self.update_stats("Protien")
    
    def remove_interaction(self, interaction):
        self.Interactions.delete_one(interaction)
        self.update_stats("Interaction")
    
    def remove_protien(self, protien):
        self.Protien.delete_one(protien)
        self.update_stats("Protien")
    
    def update_stats(self, collection):
        if collection == "Interaction":
            self.ppiDB.Statistics.Interactions = self.ppiDB.Interactions.count_documents({})
        elif collection == "Protien":
            self.ppiDB.Statistics.Protien = self.ppiDB.Protien.count_documents({})
    
    def get_sats(self):
        print("Database holds " + str(self.InteractionCount) + " interactions")
        print("Database holds " + str(self.ProtienCount) + " protiens")
        return (self.ppiDB.Statistics.Interactions, self.ppiDB.Statistics.Protien)

    def get_interactions(self):
        return self.ppiDB.Interactions.find()

    def get_protien(self):
        return self.Protien.find()

    def get_interactions_by_protien(self, protien):
        pass

    def get_interactions_by_type(self, type):
        pass

    def get_interactions_by_score(self, score):
        pass

if __name__ == "__main__":
    PPIDB = Database(27017)
    PPIDB.remove_all_interactions()
    PPIDB.remove_all_protiens()
    PPIDB.get_sats()