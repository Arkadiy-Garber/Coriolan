#!/usr/bin/env python3
import os
import statistics
from collections import defaultdict
import argparse
import textwrap
import re
import sys
# from ArkTools import *


def allButTheFirst(iterable, delim):
    x = ''
    length = len(iterable.split(delim))
    for i in range(1, length):
        x += iterable.split(delim)[i]
        x += delim
    return x[0:len(x)]


def allButTheLast(iterable, delim):
    x = ''
    length = len(iterable.split(delim))
    for i in range(0, length-1):
        x += iterable.split(delim)[i]
        x += delim
    return x[0:len(x)-1]


def remove(stringOrlist, item):
    emptyList = []
    for i in stringOrlist:
        if i != item:
            emptyList.append(i)
        else:
            pass
    outString = "".join(emptyList)
    return outString


def replace(stringOrlist, list, item):
    emptyList = []
    for i in stringOrlist:
        if i not in list:
            emptyList.append(i)
        else:
            emptyList.append(item)
    outString = "".join(emptyList)
    return outString


def lastItem(ls):
    x = ''
    for i in ls:
        if i != "":
            x = i
    return x


def deString(string):
    newString = ''
    for i in string:
        try:
            newString += str(int(i))
        except ValueError:
            break
    return newString


def capitalizeCodon(codon):
    codonOut = ''
    for i in codon:
        if i == "a":
            codonOut += "A"
        elif i == "g":
            codonOut += "G"
        elif i == "c":
            codonOut += "C"
        elif i == "t":
            codonOut += "T"
        elif i == "u":
            codonOut += "U"
        else:
            codonOut += i
    return codonOut


def fasta(fasta_file):
    seq = ''
    header = ''
    Dict = defaultdict(lambda: defaultdict(lambda: 'EMPTY'))
    for i in fasta_file:
        i = i.rstrip()
        if re.match(r'^>', i):
            if len(seq) > 0:
                Dict[header] = seq
                header = i[1:]
                header = header.split(" ")[0]
                seq = ''
            else:
                header = i[1:]
                header = header.split(" ")[0]
                seq = ''
        else:
            seq += i
    Dict[header] = seq
    # print(count)
    return Dict


parser = argparse.ArgumentParser(
    prog="antismash_helper.py",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
    ************************************************************************

    Developed by Arkadiy Garber; Middle Author Bioinformatics
    Please send comments and inquiries to ark@midauthorbio.com
    ************************************************************************
    '''))

parser.add_argument('-b', type=str, help="directory with BLAST output file", default="NA")

parser.add_argument('-f', type=str, help="input protein in FASTA format", default="NA")

parser.add_argument('-o', type=str, help="output folder", default="NA")

parser.add_argument('-n', type=str, help="number of genomes", default="NA")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(0)

args = parser.parse_known_args()[0]


faaDict = defaultdict(lambda: '-')
faa = open(args.f)
faa = fasta(faa)
for i in faa.keys():
    faaDict[i] = len(faa[i])

blastDict = defaultdict(lambda: defaultdict(lambda: '-'))
blastDir = os.listdir(args.b)
for i in blastDir:
    if lastItem(i.split(".")) == "blast":
        blast = open("%s/%s" % (args.b, i))
        for j in blast:
            ls = j.rstrip().split("\t")
            pcitLocus = ls[0]
            target = ls[1]
            perc = float(ls[2])
            alnLength = int(ls[3])
            faaLength = int(faaDict[pcitLocus])
            seq = ls[12]
            if alnLength/faaLength > 0.7 and perc > 0.7:
                if i not in blastDict[pcitLocus]:
                    blastDict[pcitLocus][i] = seq

count = 0
for i in blastDict.keys():
    if len(blastDict[i]) >= int(args.n)+1:
        out = open("%s/alignments/%s.faa" % (args.o, i), "w")
        count += 1
        for j in blastDict[i]:
            out.write(">" + allButTheLast(j, ".") + "\n")
            out.write(remove(blastDict[i][j], ["-"]) + "\n")

        out.write(">PCIT\n")
        out.write(faa[i] + "\n")

        out.close()

print("Number of core orthologs: " + str(count))




