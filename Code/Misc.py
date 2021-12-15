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
    file.readline()
    n = 1
    for line in file.readlines():
        temp = line.split("\t")
        data.set_proteins(temp[7], get_uniprot_id(temp[7]), temp[15], "")
        db.insert_protein(data.get_proteins())
        print("added protein A")
        data.set_proteins(temp[8], get_uniprot_id(temp[8]), temp[16], "")
        db.insert_protein(data.get_proteins())
        print("added protein B")
        data.set_taxons(temp[15], temp[35])
        db.insert_taxon(data.get_taxons())
        print("added taxon A")
        if temp[15] != temp[16]:
            data.set_taxons(temp[16], temp[36])
            db.insert_taxon(data.get_taxons())
            print("added taxon B")
        data.set_exps(temp[11], temp[12], temp[13], temp[14])
        db.insert_expdet(data.get_exps())
        print("added exp details")
        data.set_prim_inters(temp[22], temp[0], temp[7], temp[8], "", "")
        db.insert_interaction(data.get_prim_inters())
        print("added interaction")
        print("\n\n")
        n += 1
        if n == 6:
            break

