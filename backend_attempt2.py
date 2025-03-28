#!/bin/python3

import sys
import subprocess
import os
import re
from Bio import SeqIO
from Bio import Entrez
import pandas as pd

Entrez.email = "s2103976@ed.ac.uk"
Entrez.api_key = "a35d95f229d686c815466cf03ee2ce419b08"

def fetch_data_from_ncbi(protein_family, taxonomic_group):
    try:
        search_handle = Entrez.esearch(db="protein", term=f"{taxonomic_group}[Organism] AND {protein_family}[Protein]", retmax=10)
        search_results = Entrez.read(search_handle)
        search_handle.close()
    except Exception as e:
        print(f"Error contacting NCBI: {e}")
        sys.exit(1)
    
    prot_ids = search_results.get("IdList", [])
    if not prot_ids:
        print("No results found.")
        return None
    return prot_ids

def download_fasta(prot_ids, taxonomic_group, protein_family):
    try:
        fetch_handle = Entrez.efetch(db="protein", id=prot_ids, rettype="fasta", retmode="text")
        fetched_results = fetch_handle.read()
        fetch_handle.close()
        fetched_file_name = f"{taxonomic_group}_{protein_family}_data.fasta"
        with open(fetched_file_name, 'w') as fetched_file:
            fetched_file.write(fetched_results)
        print(f"Data written to {fetched_file_name}")
        return fetched_file_name
    except Exception as e:
        print(f"Error downloading data: {e}")
        sys.exit(1)

def analyze_motifs(fasta_file):
    fasta_to_tsv = f"{os.path.splitext(fasta_file)[0]}.tsv"
    result = subprocess.run(f"patmatmotifs -sequence {fasta_file} -outfile {fasta_to_tsv} -noprune -auto", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in patmatmotifs: {result.stderr}")
        sys.exit(1)
    
    if os.path.isfile(fasta_to_tsv):
        with open(fasta_to_tsv, "r") as tsv_file:
            records = [{'organism': re.search(r"\[([^]]*)\]", record.description).group(1), 'sequence': str(record.seq)} for record in SeqIO.parse(fasta_to_tsv, "fasta")]
        return pd.DataFrame(records)
    else:
        print(f"Error: {fasta_to_tsv} not found.")
        return None

def main(protein_family, taxonomic_group):
    prot_ids = fetch_data_from_ncbi(protein_family, taxonomic_group)
    if not prot_ids:
        return

    fasta_file = download_fasta(prot_ids, taxonomic_group, protein_family)
    motif_data = analyze_motifs(fasta_file)
    
    if motif_data is not None:
        print(motif_data)

if __name__ == "__main__":
    protein_family = sys.argv[1]
    taxonomic_group = sys.argv[2]
    main(protein_family, taxonomic_group)

