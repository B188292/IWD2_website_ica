#!/bin/python3
import sys, subprocess, time, os, re, numpy, requests, random, shutil, matplotlib, pandas, argparse
from Bio import SeqIO
from Bio import Entrez

#Conduct multiple sequence alignment using clustalo or mafft and generating the relevant plot
def MSA_runner(taxonomic_group, protein_family, prot_ids, fetched_file_name):
    aligned_sequences = f"{taxonomic_group}_{protein_family}_alignment.fasta"
    scores_file = f"{taxonomic_group}_{protein_family}_scores.txt"
    plot_file = f"{taxonomic_group}_{protein_family}_similarity_plot.png"

    if os.path.exists(aligned_sequences):
        os.remove(aligned_sequences)
    
    #Whether we use clustalo or mafft depends on the number of proteins, because clustalo can take a long time
    if len(prot_ids) < 50:
        #Use clustalo
        with open(fetched_file_name, 'r') as ffn:
            ffn.read()
            #print(f"Running ClustalO on {fetched_file_name}")
            subprocess.run(f"clustalo -i {fetched_file_name} -o {aligned_sequences} --force", shell = True,  capture_output = True, text = True)
     
    else:
        #Use mafft 
        with open(fetched_file_name, 'r') as ffn2:
             ffn2.read()
             #print(f"Running mafft")
             subprocess.run(f"mafft {fetched_file_name} > {aligned_sequences}", shell = True, capture_output = True)
    
    #Generating a graph
    #Delete previous versions of the graph for memory's sake
    if os.path.exists(f"{plot_file}.1.png"):
        os.remove(f"{plot_file}.1.png")    
    
    #Use plotcon to create the graph of the aligned sequences
    with open(aligned_sequences, 'r') as AS:
        AS.read()
       # print("Running plotcon")
        subprocess.run(f"plotcon -sequences {fetched_file_name} -winsize 20 -graph png -goutfile {plot_file}", shell = True, capture_output = True, text = True)
       # print(f"The graph is in {plot_file}")

    return

#Scan the protein sequence(s) of interest with motifs from the PROSITE database
def motif_searcher(taxonomic_group, protein_family, fetched_file_name):
    motifs = f"{taxonomic_group}_{protein_family}_motifs.tsv"
    temp_file = f"temp_{fetched_file_name}"
    motifs_csv = f"{taxonomic_group}_{protein_family}_motifs.csv"

    #Deleting any pre-existing files
    if os.path.exists(motifs):
        os.remove(motifs)
    if os.path.exists(temp_file):
        os.remove(temp_file)
    if os.path.exists(motifs_csv):
        os.remove(motifs_csv)
            
    #Removing gaps between the lines and creating a temporary file        
    with open(fetched_file_name, 'r') as ffn3:
        tf = SeqIO.parse(ffn3, "fasta")
        with open(temp_file, 'a') as tf2:
            SeqIO.write(tf, tf2, "fasta")

    #Motif scanning using patmatmotifs
    with open(temp_file, 'r') as temp:
        subprocess.run(f"patmatmotifs -sequence {temp_file} -outfile {motifs} -rformat excel -noprune -full", shell = True, capture_output = True)
    
    os.remove(temp_file)

    #Converting the motifs.tsv file to a .csv
    if os.path.exists(motifs):
       #print("motifs successfully created")
       with open(motifs, "r") as moti:
           df = pandas.read_csv(moti, sep="\t", comment="#")
           df.to_csv(motifs_csv, index = False)
           #if os.path.exists(motifs_csv) and os.path.getsize(motifs_csv) > 1:
              # print("Motifs successfuly reformatted")
           #else:
              # print("Motifs unsuccessfully reformatted")

    else:
        print("No motifs file found")

    return

#Function to conduct protein statistics analysis
def pep_statsi(taxonomic_group, protein_family, fetched_file_name):
    pepstats_output = f"{taxonomic_group}_{protein_family}_stats.txt"
    
    if os.path.exists(pepstats_output):
        os.remove(pepstats_output)

    with open(fetched_file_name, 'r') as peppy:
        peppy.read()
        #print(f"Running pepstats")
        subprocess.run(f"pepstats -sequence {fetched_file_name} -outfile {pepstats_output}", shell = True, capture_output = True, text = True)
    return
