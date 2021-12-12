    
"""
Fetch interactions for a specific gene or gene list
"""
import csv
import requests
import json
import config as cfg

request_url = cfg.BASE_URL + "/interactions"

# get file
# read_file = open('DONTEDIT\\human_protein_names.csv', 'r')
# csvreader = csv.reader(read_file)
# geneList = []
# for row in list(csvreader):
#     geneList.append(row[1])

# Sample List of genes to search for
geneList = ["STE11", "NMD4"]  # Yeast Genes STE11 and NMD4
evidenceList = ["POSITIVE GENETIC", "PHENOTYPIC ENHANCEMENT"]

# These parameters can be modified to match any search criteria following
# the rules outlined in the Wiki: https://wiki.thebiogrid.org/doku.php/biogridrest
params = {
    "accesskey": cfg.ACCESS_KEY,
    "format": "tab2",  # Return results in TAB2 format
    "geneList": "|".join(geneList),  # Must be | separated
    "searchNames": "true",  # Search against official names
    # Set to true to get any interaction involving EITHER gene, set to false to get interactions between genes
    "includeInteractors": "true",
    "taxId": 559292,  # Limit to Saccharomyces cerevisiae
    "evidenceList": "|".join(evidenceList),  # Exclude these two evidence types
    # If false "evidenceList" is evidence to exclude, if true "evidenceList" is evidence to show
    "includeEvidence": "false",
    "includeHeader": "true",
}

# Additional options to try, you can uncomment them as necessary
# params["start"] = 5 # Specify where to start fetching results from if > 10,000 results being returned
# params["max"] = 10 # Specify the number of results to return, max is 10,000
# params["interSpeciesExcluded"] = "false" # true or false, If ‘true’, interactions with interactors from different species will be excluded (ex. no Human -> Mouse interactions)
# params["selfInteractionsExcluded"] = "false" # true or false, If ‘true’, interactions with one interactor will be excluded. (ex. no STE11 -> STE11 interactions)
# params["searchIds"] = "false" # true or false, If ‘true’, ENTREZ_GENE, ORDERED LOCUS and SYSTEMATIC_NAME (orf) will be examined for a match with the geneList
# params["searchSynonyms"] = "false" # true or false, If ‘true’, SYNONYMS will be examined for a match with the geneList
# params["searchBiogridIds"] = "false" # true or false, If ‘true’, BIOGRID INTERNAL IDS will be examined for a match with the geneList
# params["excludeGenes"] = "false" # true or false, If 'true' the geneList becomes a list of genes to EXCLUDE rather than to INCLUDE
# params["includeInteractorInteractions"] = "true" # true or false, If ‘true’ interactions between the geneList’s first order interactors will be included. Ignored if includeInteractors is ‘false’ or if excludeGenes is set to ‘true’.
# params["htpThreshold"] = 50 # Any publication with more than this many interactions will be excluded
# params["throughputTag"] = "any" # any, low, high. If set to low, only `low throughput` interactions will be returned, if set to high, only `high throughput` interactions will be returned
# params["additionalIdentifierTypes"] = "SGD|FLYBASE|REFSEQ" # You can specify a | separated list of additional identifier types to search against (see get_identifier_types.py)

r = requests.get(request_url, params=params)
interactions = r.text
interactions = interactions.split("\n")
for  i in range(len(interactions)):
    interactions[i] = interactions[i].split("\t")
