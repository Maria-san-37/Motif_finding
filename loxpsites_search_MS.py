!usr/bin/env python3
# -- coding: utf-8 --
#
# ------------------------------
# Name: motif_search.py
# Purpose:
# Find lopxpsites in fasta files 
# Author: Maria del Carmen Sanchez
# INPUT: file.fastq

# OUTPUT: file.fa
# motif-loxpsym: ATAACTTCGTATATGTACATTATACGAAGTTAT
# Name: Maria del Carmen Sanchez

# Created: September-2022

# ------------------------------
import argparse
import itertools
import sys
import regex
import re
import pandas as pd

parser= argparse.ArgumentParser(description="Read input files")
parser.add_argument("--fasta","-s",
        metavar="FILE",
        required=True,
        help="fasta file to split reads if they have a loxpsym site")
args=parser.parse_args()
loxpsym_pattern = regex.compile(r'(ATAACTTCGTATATGTACATTATACGAAGTTAT){e<=10}',re.I) #ataacttcgtataatgtacattatacgaagttat
#character_wildcard=re.compile('.')
count=0
direction="+"
name_input=args.fasta.split('.fasta')
name_input=name_input[0]
count=0
with open(args.fasta) as f_input, open(name_input+'filter_1.fasta', 'w') as f_output:
    for line1,line2 in itertools.zip_longest(*[f_input]*2):
        if line1.startswith('>') and line2.startswith('A' or 'C' or 'T' or 'G'):
            if regex.search(loxpsym_pattern,line2):
                print(regex.search(loxpsym_pattern,line2))
                f_output.write(line1+"\n"+line2+"\n")
                print(line1+"\n")
            else:
                pass
        else:
            pass
    print("the total number of loxpsym sites found is %r" %count)
