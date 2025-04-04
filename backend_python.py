#!/bin/python3

import sys, subprocess, datetime, os, re, numpy, requests, random, shutil, matplotlib, pandas, argparse
import functions as f
from Bio import SeqIO
from Bio import Entrez

#Part 1: Obtain user data from the .php file and send the information to NCBI to obtain the datasets
#1a  Ask the user for the protein and taxonomic group
#user_id = sys.argv[1]
#protein_family = ' '.join(sys.argv[1:-3])
#if protein_family is null:
 #   protein_family = "glucose-6-phosphatase"
#taxonomic_group = ' '.join(sys.argv[2:-2])
#if taxonomic_group is null:
 #   taxonomic_group = "Aves"

#protein_family = sys.argv[1].strip('"\'')  # Handles 'homo sapiens'
#taxonomic_group = sys.argv[2].strip('"\'')

protein_family = sys.argv[1] or "glucose-6-phosphatase"
taxonomic_group = sys.argv[2] or "Aves"

#1b  The necessary information to send the information to NCBI
Entrez.email = "s2103976@ed.ac.uk"
Entrez.api_key = "a35d95f229d686c815466cf03ee2ce419b08"

#1c  Sending the initial query to NCBI to get the IDs
search_handle = Entrez.esearch(db = "protein", term = f'"{taxonomic_group}"[Organism] AND "{protein_family}"[Protein]')
search_results = Entrez.read(search_handle)
search_handle.close()

#1d Using the IDs generated from the first search to obtain fasta files from the protein
prot_ids = search_results["IdList"]
if len(prot_ids) < 1:
    #print("Sorry, no results were found.")
    sys.exit()
else:    
    fetch_handle = Entrez.efetch(db="protein", id = prot_ids, rettype="fasta", retmode="text")
    fetched_results = fetch_handle.read()
    fetch_handle.close()
    
    fetched_file_name = f"{taxonomic_group}_{protein_family}_data.fasta"
    
    with open(fetched_file_name, 'w') as fetched_file:
        fetched_file.write(fetched_results)
    #print(f"Search results have been written to {fetched_file_name}")


#Steps 2, 3, and 4: Perform analysis on the obtained dataset to determine the level of conservation across the species within that taxonomic group and produce the relevant plots. Scan the protein sequence(s) of interest with motifs from the PROSITE database. Also perform additional tests

#2a Establishing variables from the checkboxes
MSA = sys.argv[3] #This is for the conservation analysis
PD = sys.argv[4] #This is for the PROSITE motif scanning
PS = sys.argv[5] #This is for protein analysis

#Multiple Sequence alignment -> Relevant to Part 2
if MSA == '1':
    f.MSA_runner(taxonomic_group, protein_family, prot_ids, fetched_file_name)
     #aligned_sequences = f"{taxonomic_group}_{protein_family}_alignment.fasta"
     #plot_file = f"{taxonomic_group}_{protein_family}_similarity_plot.png.1.png"

#PROSITE MOTIF Search -> Relevant to Part 3
if PD == '1':
    f.motif_searcher(taxonomic_group, protein_family, fetched_file_name)
    #motifs_tsv = f"{taxonomic_group}_{protein_family}_motifs.tsv"
    #motifs_csv = f"{taxonomic_group}_{protein_family}_motifs.csv"

#Protein Statistics -> Extra Analysis for Part 4
if PS == '1':
    f.pep_statsi(taxonomic_group, protein_family, fetched_file_name)
    #pepstats_output = f"{taxonomic_group}_{protein_family}_stats.txt"

#Taking the output from all the tests and putting it in a .zip folder
output_zip = f"{taxonomic_group}_{protein_family}_results.zip"
#output_directory = os.getcwd()

if os.path.exists(output_zip):
    os.remove(output_zip)

#for filename in os.listdir('.'):
#    if filename.startswith(taxonomic_group) and filename.endswith('.txt', '.csv', '.tsv', '.fasta', '.png'):
#        with open(output_zip, 'w') as oz:
#            subprocess.call(f"zip {output_zip}", shell = True)

#output_zip = f"{taxonomic_group}_{protein_family}_results.zip"
files = [f for f in os.listdir('.')
         if f.startswith(taxonomic_group)
         and f.endswith(('.txt', '.csv', '.tsv', '.fasta', '.png'))]

if files:
    subprocess.run(f"zip {output_zip} {' '.join(files)}", shell=True, stdout=subprocess.DEVNULL)
    #print(f"Created {output_zip}")
else:
    print("No files to zip")

# Move all relevant files into the new directory
#for filename in os.listdir('.'):
#    if filename.startswith(taxonomic_group) and filename.endswith(('.txt', '.csv', '.tsv', '.fasta', 'png')
#        shutil.move(filename, os.path.join(output_directory, filename))

#os.makedirs(output_directory, exist_ok=True)

#zip_filename = f"{taxonomic_group}_{protein_family}_results.zip"
#shutil.make_archive(base_name=os.path.join(os.getcwd(), f"{taxonomic_group}_{protein_family}_results"),format='zip', root_dir=output_directory)

#print(f"All results have been zipped to {zip_filename}")

#output_zip = f"{user_id}_{taxonomic_group}_{protein_family}_all_data"
#output_directory = "/home/s2103976/public_html/ICA/results"
#shutil.make_archive(output_zip, 'zip', output_directory)

#output_dir = os.path.join('results', f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
#os.makedirs(output_dir, exists_ok = True)

#os.chmod(fetched_file_name, 0o755)
#os.chmod(new_fasta, 0o755)
#os.chmod(fasta_totsv, 0o755)
