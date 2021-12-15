import pymongo
client = pymongo.MongoClient("mongodb+srv://user:qwerty321@ppidb.3pazw.mongodb.net/PPIdb?retryWrites=true&w=majority")
db = client.test

# # file_loc = "Datasets\human-prot\string-all-prot.txt"
# # string_prot = open(file_loc, 'r')
# # print(string_prot.readline())

# #!/usr/bin/env python3

# ##########################################################
# ## For a given list of proteins the script resolves them
# ## (if possible) to the best matching STRING identifier
# ## and prints out the mapping on screen in the TSV format
# ##
# ## Requires requests module:
# ## type "python -m pip install requests" in command line
# ## (win) or terminal (mac/linux) to install the module
# ###########################################################

# import requests ## python -m pip install requests

# string_api_url = "https://version-11-5.string-db.org/api"
# output_format = "tsv-no-header"
# method = "get_string_ids"

# ##
# ## Set parameters
# ##

# params = {

#     "identifiers" : "BRCA1", # your protein list
#     "species" : 9606, # species NCBI identifier 
#     "limit" : 1, # only one (best) identifier per input protein
#     "echo_query" : 1, # see your input identifiers in the output
#     "caller_identity" : "www.awesome_app.org" # your app name

# }

# ##
# ## Construct URL
# ##


# request_url = "/".join([string_api_url, output_format, method])

# ##
# ## Call STRING
# ##

# results = requests.post(request_url, data=params)

# ##
# ## Read and parse the results
# ##

# for line in results.text.strip().split("\n"):
#     l = line.split("\t")
#     input_identifier, taxonId, taxonName = l[0], l[3], l[4]
#     print("Input:", input_identifier, "Taxon ID:", taxonId,"Taxon:", taxonName, sep="\t")

# # import urllib.parse
# # import urllib.request

# # url = 'https://www.uniprot.org/uploadlists/'

# # params = {
# # 'from': 'GENENAME',
# # 'to': 'ACC',
# # 'format': 'tab',
# # 'query': 'MDH1'
# # }

# # data = urllib.parse.urlencode(params)
# # data = data.encode('utf-8')
# # req = urllib.request.Request(url, data)
# # with urllib.request.urlopen(req) as f:
# #    response = f.read()
# # print(response.decode('utf-8').split("\n")[1].split("\t")[1])

