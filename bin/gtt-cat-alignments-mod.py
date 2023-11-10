#!/usr/bin/env python
# THIS SCRIPT WAS TAKEN FROM THE GTOTREE PACKAGE BY MIKE LEE: https://github.com/AstrobioMike/GToTree

import sys
from glob import glob
import argparse
import os.path

parser = argparse.ArgumentParser(description='This script is a helper script to concatenate fasta-formatted multiple sequence alignment files, and generate partitions file.')

required = parser.add_argument_group('required arguments')

required.add_argument("-t", "--tmp-dir", help="The working tmp_dir for the current GToTree run", action="store", dest="tmp_dir", required=True)
required.add_argument("-o", "--output-dir", help="The output_dir for the current GToTree run", action="store", dest="output_dir", required=True)
parser.add_argument("--nucleotides", help="Provide this flag if user specified nucleotide mode", action="store_true")


if len(sys.argv)==1:
  parser.print_help(sys.stderr)
  sys.exit(0)

args = parser.parse_args()

tmp_dir = args.tmp_dir + "/"
output_dir = args.output_dir + "/"

# getting list of all alignment files
if not args.nucleotides:

    list_of_alignment_files = glob(tmp_dir + "*.fa")

else:
    list_of_alignment_files = glob(tmp_dir + "*.fa")

# initializing dictionary that will hold headers as keys and a list of all seqs to be cat'd as values
dict_of_genomes = {}

print(list_of_alignment_files)
# getting headers (they are the same in all files and all are found in all files at this point, so only need to pull from one)
with open (list_of_alignment_files[0]) as file:
    print(list_of_alignment_files[0])
    for line in file:
        if line.strip().startswith(">"):
            print((line.strip().lstrip(">")))
            dict_of_genomes[(line.strip().lstrip(">"))] = []


print("===========================")
# iterating through all files adding seqs
for file in list_of_alignment_files:
    print(file)
    with open(file) as fasta:
        curr_header=""
        for line in fasta:
            line = line.strip()
            if line.startswith(">"):
                curr_header=line.lstrip(">")
            else:
                # print(curr_header)
                dict_of_genomes[curr_header].append(line)


# writing out concatenated (horizontally) sequence file

if not args.nucleotides:
    with open(output_dir + "Aligned_SCGs.fa", "w") as out:
        for header, seqs in dict_of_genomes.items():
            out.write(">" + header + "\n")
            out.write("XXXXX".join(seqs) + "\n")

else:
    with open(output_dir + "Aligned_SCGs.fa", "w") as out:
        for header, seqs in dict_of_genomes.items():
            out.write(">" + header + "\n")
            out.write("NNNNNN".join(seqs) + "\n")

# making partitions file
    # getting list of gene names in order they were cat'd together
if not args.nucleotides:
    gene_list = [os.path.basename(x)[:-3] for x in list_of_alignment_files]
    print(gene_list)
else:
    gene_list = [os.path.basename(x)[:-3] for x in list_of_alignment_files]

   # all are same length, so just need one genome entry, then to count the bases per element in dict values list, and add 5 for the XXXXX spacers
   # getting all alignment lengths

alignment_lengths_list = [len(x) for x in list(dict_of_genomes.values())[0]]

curr_start = 1
curr_stop = 0

with open(output_dir + "Partitions.txt", "w") as out:
    for i in range(0,len(gene_list)):
        curr_stop = curr_start + alignment_lengths_list[i] - 1

        if not args.nucleotides:
            out.write("AA, " + str(gene_list[i]) + " = " + str(curr_start) + "-" + str(curr_stop) + "\n")
            curr_start = curr_stop + 6
        else:
            out.write("DNA, " + str(gene_list[i]) + " = " + str(curr_start) + "-" + str(curr_stop) + "\n")
            curr_start = curr_stop + 7