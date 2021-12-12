import pyrebase
import csv
import urllib.request as urllib
from bs4 import BeautifulSoup
import threading
import time
import logging
import psutil
import requests
import json
import config as cfg

def get_protein_interactions(gene_name):
    request_url = cfg.BASE_URL + "/interactions"
    evidenceList = ["POSITIVE GENETIC", "PHENOTYPIC ENHANCEMENT"]

    # These parameters can be modified to match any search criteria following
    # the rules outlined in the Wiki: https://wiki.thebiogrid.org/doku.php/biogridrest
    params = {
        "accesskey": cfg.ACCESS_KEY,
        "format": "tab2",  # Return results in TAB2 format
        "geneList": gene_name,  # Must be | separated
        "searchNames": "true",  # Search against official names
        # Set to true to get any interaction involving EITHER gene, set to false to get interactions between genes
        "includeInteractors": "true",
        "taxId": 559292,  # Limit to Saccharomyces cerevisiae
        "evidenceList": "|".join(evidenceList),  # Exclude these two evidence types
        # If false "evidenceList" is evidence to exclude, if true "evidenceList" is evidence to show
        "includeEvidence": "false",
        "includeHeader": "true",
    }
    r = requests.get(request_url, params=params)
    interactions = r.text
    interactions = interactions.split("\n")
    for  i in range(1, len(interactions)):
        temp = interactions[i].split("\t")
        if(len(temp) != 0):
            try:
                interaction = {
                        "geneA": temp[7] if len(temp) > 7 else "",
                        "geneB": temp[8] if len(temp) > 8 else "",
                        "exp-system": temp[11] if len(temp) > 11 else "",
                        "exp-system-type": temp[12] if len(temp) > 12 else "",
                        "pubmed-id": temp[14] if temp[14] != "-" else "",
                        "oraganismA": temp[15] if len(temp) > 15 else "",
                        "oraganismB": temp[16] if len(temp) > 16 else "",
                        "sourceDB": temp[22] if len(temp) > 22 else "",
                        "inter-species": True if temp[15] == temp[16] else False
                    }
                interID = temp[0]
                db.child("interactions/" + interID).push(interaction)
            except IndexError as e:
                print(e)
                pass
        

def get_protein_name(url):
    """
    Given a url, extract the protein name from the url
    """
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def tableDataText(url):
    # soup = BeautifulSoup(html, parser='html.parser')
    """Parses a html segment started with tag <table> followed 
    by multiple <tr> (table rows) and inner <td> (table data) tags. 
    It returns a list of rows with inner columns. 
    Accepts only one <th> (table header/data) in the first row.
    """
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    [script.extract() for script in soup(["script", "style", "span class=\"tooltipped\""])]
    return soup.find("div", {"id": "names_and_taxonomy"}).find("table").findAll("tr")
    
   
    
"""Set up firebase"""
pyrebase_config = {
    "apiKey": "AIzaSyB97xXrED09JJoEZqmEdAN1PlAL-CBLeeM",
    "authDomain": "ppidb-b0ac7.firebaseapp.com",
    "databaseURL": "https://ppidb-b0ac7-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "ppidb-b0ac7",
    "storageBucket": "ppidb-b0ac7.appspot.com",
    "messagingSenderId": "113239765206",
    "appId": "1:113239765206:web:bb75ee1548eab999089977",
    "measurementId": "${config.measurementId}",
}

firebase = pyrebase.initialize_app(pyrebase_config)
db = firebase.database()

def sendtoDB(start, end):
    read_file = open('DONTEDIT/uniprot_proteins.csv', 'r')
    csvreader = csv.reader(read_file)
    next(csvreader)
    for i in (range(0, start)):
        next(csvreader)
    for i in range(start, end):
        row = next(csvreader)
        data = {
                "uniprotID": row[0].split('/')[-1],
                "link": row[0],
                "species": "",
                "organ": "",
                "function": "",
            }
        # soup = tableDataText(row[0])
        soup = get_protein_name(row[0])
        [script.extract() for script in soup(
            ["script", "style", "a", "<div id=\"bottom\" >"])]
        text = soup.findAll(text=True)
        # print(soup)
        for i in range(len(text)):
            if(text[i] == 'Gene'):
                gene = text[i+1]
            if(text[i] == 'Organism'):
                data['species'] = text[i+1]
        if (gene == 'N/A'):
            break

        db.child("protiens/" + gene).set(data)
        get_protein_interactions(gene)

    read_file.close()


if __name__ == "__main__":
    NUM_THREADS = psutil.cpu_count(logical=False)
    csvreader = csv.reader(open('DONTEDIT/uniprot_proteins.csv', 'r'))
    totalData = len(list(csvreader))
    print(totalData)
    threads = []
    
    for i in range(NUM_THREADS):
        startindex = i*(totalData//NUM_THREADS)
        if (i == NUM_THREADS-1):
            endindex = totalData
        else:
            endindex = (i+1)*(totalData//NUM_THREADS)
        threads.append(threading.Thread(target=sendtoDB, args=(startindex, endindex)))
        print("Thread " + str(i) + " started with", startindex, endindex)
        logging.log(logging.INFO, "Thread " + str(i) + " started")
        threads[i].start()
        time.sleep(1)

    for i in range(NUM_THREADS):
        threads[i].join()
        print("Thread " + str(i) + " finished")