#! /bin/bash

function usage() {
    cat <<USAGE

    Usage: $0 [-f ref] [-t thr] [-s sys] [-o out] [-n num]

    Options:
        -d, --dir:   directory with FASTA files (nucleotide)
        -r, --ref:      reference proteins in FASTA format
        -o, --out:      output folder name
        -x, --ext:      filename extension for genome FASTA files
        -t, --thr:      number of parallel cores (2)

USAGE
    exit 1
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

EXT="fa"
THR=2
OUT="coregene"
while [ "$1" != "" ]; do
    case $1 in
    -d | --dir)
        shift
        DIR=$1
        ;;
    -r | --ref)
        shift
        REF=$1
        ;;
    -o | --out)
        shift
        OUT=$1
        ;;
    -t | --thr)
        shift
        THR=$1
        ;;
    -x | --ext)
        shift
        EXT=$1
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


if [[ ${DIR} == "" ]]; then
    echo 'Please provide directory with genome FASTA files via the -d argument';
    exit 1;
fi

if [[ ${REF} == "" ]]; then
    echo 'Please provide reference protein sequences via the -r argument';
    exit 1;
fi

mkdir -p ${OUT}
mkdir -p ${OUT}/alignments

for i in ${DIR}/*${EXT}; do
    echo ${i}
    autodetect_blast_db.sh -f ${i}
    tblastn -out ${i%.*}.blast -max_target_seqs 1 -num_threads ${THR} -query ${REF} -db ${i} -outfmt "6 qseqid sseqid pident length qlen slen qstart qend sstart send evalue qseq sseq"
done

NUM=$(ls -1 ${DIR}/*${EXT} | wc -l)

coregene.py -b ${DIR} -f ${REF} -o ${OUT} -n ${NUM}

for i in ${OUT}/alignments/*faa; do
    muscle -align ${i} -output ${i%.*}.fa
done

gtt-cat-alignments-mod.py -t ${OUT}/alignments -o ${OUT}

FastTree ${OUT}/Aligned_SCGs.fa > ${OUT}/Aligned_SCGs.tre






