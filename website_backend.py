#!/bin/python3

#importing the necessary things
import subprocess, time, sys, os, re, numpy, requests, shutil, random
from Bio import SeqIO
from Bio import Entrez
import requests
import matplotlib

subprocess.run("sh -c $(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)", shell = True)
subprocess.run("export PATH=${PATH}:${HOME}/edirect")

#Here we're creating variables that store the protein family and taxonomic group that the host is interested in
#protein_family = input("Please enter the protein family name (e.g., glucose-6-phosphatase")
#here you have to make it so that if the user enters something incorrect, the ssystem suggests something similar. 

#GETting the protein and taxon information from the analytis.php file
analytis_url = "https://bioinfmsc8.bio.ed.ac.uk/~s2103976/ICA/analytis.php"
parameters = {"protein_family":"prot fam", "taxon_group" : "tax fam"}
protaxon = requests.get(analytis_url, paramters)
if protaxon.status_code == 200:
    protaxon_info = protaxon.json()

#connecting to NCBI using the e-utilities package
#prot_family = sys.argv[1] if len(sys.argv) > 1 else "glucose-6-phosphatase"
#taxon_group = sys.argv[2] if len(sys.argv) > 1 else random.choice("Aves", "aves")

print("Hello world")


subprocess.run("sh -c $(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)")

Entrez.email = "s2103976@ed.ac.uk"
Entrez.tool = "biopython"
search_handle = Entrez.search(db = "protein", term = f"{species}[Organism] AND {protein}[Protein]", retmax = 100)
search_results = Entrez.read(search_handle)
Entrez.api_key = "a35d95f229d686c815466cf03ee2ce419b08"
search_handle.close()



