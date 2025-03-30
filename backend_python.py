#!/bin/python3

import sys, subprocess, time, os, re, numpy, requests, random, shutil, matplotlib, pandas, argparse
from Bio import SeqIO
from Bio import Entrez

#Part 1: Obtain user data from the .php file and send the information to NCBI to obtain the datasets
#1a  Ask the user for the protein and taxonomic group
protein_family = sys.argv[1]
taxonomic_group = sys.argv[2]


#1b  The necessary information to send the information to NCBI
Entrez.email = "s2103976@ed.ac.uk"
Entrez.api_key = "a35d95f229d686c815466cf03ee2ce419b08"

#1c  Sending the initial query to NCBI to get the IDs
search_handle = Entrez.esearch(db = "protein", term = f"{taxonomic_group}[Organism] AND {protein_family}[Protein]", retmax = 10)
search_results = Entrez.read(search_handle)
search_handle.close()

#1d Using the IDs generated from the first search to obtain fasta files from the protein
prot_ids = search_results["IdList"]
if len(prot_ids) < 1:
    print("Sorry, no results were found.")

else:    
    fetch_handle = Entrez.efetch(db="protein", id = prot_ids, rettype="fasta", retmode="text")
    fetched_results = fetch_handle.read()
    fetch_handle.close()
    
    fetched_file_name = f"{taxonomic_group}_{protein_family}_data.fasta"
    
    with open(fetched_file_name, 'w') as fetched_file:
        fetched_file.write(fetched_results)
    print(f"Search results have been written to {fetched_file_name}")


#Step 2: Perform analysis on the obtained dataset to determine the level of conservation across the species within that taxonomic group and produce the relevant plots
#2.a Using clustalo to align the sequences
aligned_sequences = f"{taxonomic_group}_{protein_family}_alignment.fasta"
scores_file = f"{taxonomic_group}_{protein_family}_scores.txt"
plot_file = f"{taxonomic_group}_{protein_family}_plot.png"

with open(aligned_sequences, 'w') as AS:
    subprocess.run(["clustalo", "-i", "fetched_file_name", "-o", "aligned_sequences", "--force"])

subprocess.run(["plotcon", "-sequences", "aligned_sequences", "-scores", "scores_file", "-graph", "png", "-goutfile", "plot_file"])


#2.b Message to the user
print(f"Aligned sequences saved to {aligned_sequences}.")
print(f"{taxonomic_group}_{protein_family}_output.txt")
#subprocess.call(f"cat {aligned_sequences}")

#Step 3: Connecting to PROSITE using patmatmotifs
#3a open the fasta file and create a new file with all the sequences
os.chmod(fetched_file_name, 0o777)
with open(f"{fetched_file_name}", "r") as fastalavista:
    new_fasta = "new_data.fasta"
    #print(new_fasta)

    with open(new_fasta, "a") as new_file:
        for y in SeqIO.parse(fastalavista, "fasta"):
            SeqIO.write(y, new_file, "fasta")
    
#    os.chmod(new_fasta, 0o777)
    print(f"FASTA file created: {os.path.abspath(new_fasta)}")

#Running patmatmotifs to scan the .fasta file
fasta_to_tsv = f"{taxonomic_group}_{protein_family}_data.tsv"
#fasta_to_tsv = os.path.join(os.getcwd(), f"{taxonomic_group}_{protein_family}_data.tsv")
subprocess.run(f"patmatmotifs -sequence {new_fasta} -outfile {fasta_to_tsv} -noprune", shell = True)

if os.path.isfile(fasta_to_tsv):
    os.chmod(fasta_to_tsv, 0o777)
    print("Motif search is complete.")
    with open(fasta_to_tsv, "r") as tsv_file:
        records = [{'organism': re.search(r"\[([^]]*)\]", record.description).group(1), 'sequence': str(record.seq)} for record in SeqIO.parse(fasta_to_tsv,"fasta")]
        the_dataframe = pandas.DataFrame(records)
        print(the_dataframe)

else:
    print("No .tsv file found")

#if os.path.isfile(fasta_to_tsv):
   # print(f"{fasta_to_tsv} exists")
   # subprocess.run(f"patmatmotifs -sequence {new_fasta} -outfile {fasta_to_tsv} -noprune", shell = True)
#    print("Motif search complete.")

#else:
#    print("No .tsv file.")

#subprocess.run(f"patmatmotifs -sequence {new_fasta} -outfile {fasta_to_tsv} -noprune -auto -rformat excel", shell = True)
#subprocess.run(f"patmatmotifs -sequence {new_fasta} -outfile {fasta_to_tsv} -noprune", shell = True)
#os.chmod(fasta_to_tsv, 0o777)
#print(fasta_to_tsv)

#if os.path.isfile(fasta_to_tsv):
#    with open(fasta_to_tsv, "r") as tsv_file:
#        records = [{'organism': re.search(r"\[([^]]*)\]", record.description).group(1), 'sequence': str(record.seq)} for record in SeqIO.parse(fasta_to_tsv,"fasta")]
#        the_dataframe = pandas.DataFrame(records)
#        print(the_dataframe)
#else:
#    print("No file found")

#os.chmod(fetched_file_name, 0o755)
#os.chmod(new_fasta, 0o755)
#os.chmod(fasta_totsv, 0o755)
