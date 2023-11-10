## Coriolan
This software takes two inputs:
 - a folder containing genomes (in FASTA format)
 - a file with reference proteins (also in FASTA format)

The reference proteins are queried via tBLASTn against the genome sequences to identify orthologs, which are then aligned with Muscle, concatenated with a GToTree helper script, and used to generate a Newick-formatted phylogenomic tree using FastTree.

### Installation (Conda required):

    git clone https://github.com/Arkadiy-Garber/Coriolan.git
    cd Coriolan
    bash install.sh
    conda activate coriolan

### Quick-start

    coriolan -d assemblies/ -x fa -r reference_proteins.faa -o output_folder -t 16

 - The above **assemblies/** folder contains nucleotide FASTA files, with filenames ending in _.fa_.
 - The **reference_proteins.faa** file is a multi-FASTA file containing trusted protein sequences to use in the phylogeny.
