## Coriolan


### Installation (from ~/bin):

    git clone https://github.com/Arkadiy-Garber/Coriolan.git
    cd Coriolan
    bash install.sh
    conda activate gtotree

### Quick-start

    coriolan -d assemblies/ -x fa -r reference_proteins.faa -o output_folder -t 16

The above assemblies/ folder contains nucleotide FASTA files, with filenames ending in ".fa". The reference_proteins.faa file is a multi-FASTA file containing trusted protein sequences to use in the phylogeny.
