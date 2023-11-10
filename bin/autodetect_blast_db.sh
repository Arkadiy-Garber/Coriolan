#!/bin/bash

#! /bin/bash

function usage() {
    cat <<USAGE

    Usage: $0 [-f fasta]

    Options:
        -f, --fasta:   genome in FASTA format

USAGE
    exit 1
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

while [ "$1" != "" ]; do
    case $1 in
    -f | --fasta)
        shift
        FASTA=$1
        ;;
    -h | --help)
        usage
        ;;
    *)
        usage
        exit 1
        ;;
    esac
    shift
done

# Prompt the user for the FASTA file path
fasta_file=${FASTA}

# Extract the directory and base name of the FASTA file
fasta_dir=$(dirname "$fasta_file")
fasta_name=$(basename -- "$fasta_file")
fasta_base="${fasta_name%.*}"

# Expected BLAST database file extensions (you can add more if needed)
#db_extensions=("ntf" "nto" "ndb" "nhr" "nin" "nsq")
db_extensions=("nhr" "nin" "nsq")
# Initialize a flag to check if a BLAST database was found
db_found=false

# Iterate through the expected extensions and check for associated files
for ext in "${db_extensions[@]}"; do
    db_file="${fasta_file}.${ext}"
    if [ -f "${db_file}" ]; then
        #echo "Found associated BLAST database file: ${fasta_dir}/${db_file}"
        db_found=true
    fi
done

# Check if a BLAST database was found
if [ "$db_found" = false ]; then
    echo "No associated BLAST database files found for $fasta_file"
    makeblastdb -dbtype nucl -in ${fasta_file} -out ${fasta_file}
fi

