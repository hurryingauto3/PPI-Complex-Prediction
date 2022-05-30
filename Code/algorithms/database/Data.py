class Data:
    def __init__(self) -> None:
        self.inter_data = {
            "_id": "",
            "Source": "",
            "Database ID": "",  # the id of the interaction in the database source for the interaction
            "Gene A": "",  # the official symbol A for protein A
            "Gene B": "",  # the official symbol A for protein B
            "MINT Score": "",  # MINT score for the interaction
            # primary or secondary data (produced by our algo)
            "Type of data": "",
            # predicted score for interaction produced by our algo (is "-" if primary)
            "Predicted Score": "",
            "Experiment ID": ""  # _id in the experiment table for the interaction
        }

        self.protein_data = {
            "_id": "",
            "Gene": "",
            "UniprotKB AC": "",
            "Taxon ID": "",
            "Description": ""
        }

        self.taxon_data = {
            "_id": "",
            "Taxon ID": "",
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

    def set_inters(self, source, db_id, GeneA, GeneB, score, type, pred_score, exp_id):
        self.inter_data["_id"] = GeneA+"_"+GeneB
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
        self.exp_data["_id"] = pubmed
        self.exp_data["Experimental System"] = sys
        self.exp_data["Experiment System Type"] = sys_type
        self.exp_data["Author"] = author
        self.exp_data["Publication Source (PubMed ID)"] = pubmed
