#!/usr/bin/python
import urllib.request as urllib
from bs4 import BeautifulSoup
import csv
import threading
import time


def get_protein_name(url):
    """
    Given a url, extract the protein name from the url
    """
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


read_file = open('Datasets/DONTEDIT/uniprot_proteins.csv', 'r')
csvreader = csv.reader(read_file)
write_file = open('../human-prot/human_protein_names_3.csv', 'w')
csvwriter = csv.writer(write_file)
header = next(csvreader)
# print(header)
count = 0
flag = False

for row in list(csvreader):
    write_row = []
    for protein_web in row:
        write_row.append(protein_web)
        soup = get_protein_name(protein_web)
        [script.extract() for script in soup(
            ["script", "style", "a", "<div id=\"bottom\" >"])]
        text = soup.findAll(text=True)
        text = " ".join(text)
        print(text.find("Gene"))
        print(text[text.find("Gene")])
        break
        # write_row.append(text[text.find("Gene") + 1])
    csvwriter.writerow(write_row)
    count += 1
    print(count)
    break
read_file.close()
write_file.close()
