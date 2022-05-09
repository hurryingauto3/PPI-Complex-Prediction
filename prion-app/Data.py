class Data: 
    def __init__(self) -> None:
        self.prim_inter_data = {
            "Source" : "",
            "Database ID" : "", #the id listed in the database source for the interaction
            "Gene A" : "", #the official symbol A for protein A
            "Gene B" : "", #the official symbol A for protein B
            "MINT Score" : "", #MINT score for the interaction
            "Experiment Data" : "" #info on exp details key
        }
        
        self.sec_inter_data = {
            "Source" : "",
            "Database ID" : "", #the id listed in the database source for the interaction
            "Gene A" : "", #the official symbol A for protein A
            "Gene B" : "", #the official symbol A for protein B
            "MINT Score" : "", #MINT score for the interaction
            "Predicted Score" : "", #score from ensemble
            "Experiment Data" : "" #info on exp details key
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
    
    def set_prim_inters(self, source, db_id, geneA, geneB, score, exp_k):
        self.prim_inter_data["Source"] = source
        self.prim_inter_data["Database ID"] = db_id
        self.prim_inter_data["Gene A"] = geneA
        self.prim_inter_data["Gene B"] = geneB
        self.prim_inter_data["MINT Score"] = score
        self.prim_inter_data["Experiment Data"] = exp_k
        
    def set_sec_inters(self, source, db_id, geneA, geneB, score, pred_score, exp_k):
        self.sec_inter_data["Source"] = source
        self.sec_inter_data["Database ID"] = db_id
        self.sec_inter_data["Gene A"] = geneA
        self.sec_inter_data["Gene B"] = geneB
        self.sec_inter_data["MINT Score"] = score
        self.sec_inter_data["Predicted Score"] = pred_score
        self.prim_inter_data["Experiment Data"] = exp_k
        
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

        