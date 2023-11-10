## Coriolan


### Installation (from ~/bin):

    git clone https://github.com/Arkadiy-Garber/Coriolan.git
    conda create -y -n gtotree -c astrobiomike -c conda-forge -c bioconda -c defaults gtotree --yes
    conda activate gtotree
    export PATH="${HOME}/bin/Coriolan/bin:$PATH"

This software is currently nestled inside the conda environment of the [GToTree](https://github.com/AstrobioMike/GToTree) software.

### Quick-start

    coriolan -d assemblies/ -x fa -r reference_proteins.faa -o output_folder -t 16

The above assemblies/ folder contains nucleotide FASTA files, with filenames ending in ".fa". The reference_proteins.faa file is a multi-FASTA file containing trusted protein sequences to use in the phylogeny.
