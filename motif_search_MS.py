#!usr/bin/env python3
# -- coding: utf-8 --
#
# ------------------------------
# Name: motif_search.py
# Purpose:
# Find lopxpsites in synthetic chromosomes that come from assemblies
# Author: Maria del Carmen Sanchez
# INPUT: file.fa  either the reference genome or the sample to look for the loxpsites and divide the file into LUs or segments

# OUTPUT: file.fa file divided into LUs or segments
# motif-loxpsym: ATAACTTCGTATATGTACATTATACGAAGTTAT
# Name: Maria del Carmen Sanchez

# Created: September-2022

# ------------------------------

import argparse
import re

parser= argparse.ArgumentParser(description="Read input files")
parser.add_argument("--sample","-s",
        metavar="FILE",
        required=True,
        help="fasta file the genome or sample to divide into LU's ")
args=parser.parse_args()
r = re.compile("ATAACTTCGTATAATGTACATTATACGAAGTTAT",re.I) #ataacttcgtataatgtacattatacgaagttat
count=0
direction="+"
name_input=args.sample.split('.fa')
name_input=name_input[0]
print("Spliting file into LU.....%s"%name_input)
with open(args.sample) as f_input, open(name_input+'_sline.fa', 'w') as f_output:
    block = []
    for line in f_input:
        if line.startswith('>'):
            if block:
                f_output.write(''.join(block) + '\n')
                block = []
            f_output.write(line)
        else:
            block.append(line.strip())

    if block:
        f_output.write(''.join(block) + '\n')
lista_LU=[]
list_start=[]
list_end=[]
with open(name_input+'_sline.fa','r') as sample:
    for linea in sample.readline():
        for line in sample:
            line=line.strip()
            chunks = re.split('ATAACTTCGTATAATGTACATTATACGAAGTTAT', line, flags=re.IGNORECASE)
            #lista_LU.append(chunks)
            for LU in chunks:
                lista_LU.append(LU)
            match=re.finditer(r'ATAACTTCGTATAATGTACATTATACGAAGTTAT',line,flags=re.IGNORECASE)
            for m in match:
                #print(m.span())
                start=m.span()[0]
                list_start.append(start)
                end=m.span()[0]
                list_end.append(end)
                #print(end)

list_start.insert(0,1)
#list_end.insert(0,376)
#print(list_start)
#print(list_end)
count=0
with open(name_input+'LUs.fa','w') as output:
    for i in range(0,len(list_start)):
        for k in range(0,len(list_end)):
            for j in range(0,len(lista_LU)):
                if i==k==j:
                    count=count+1
                    #print(">LU_%s_start_%s_end_%s\n"%(count,list_start[i],list_end[k]))
                    output.write(">LU_%s_start_%s_end_%s\n"%(count,list_start[i],list_end[k]))
                    output.write(lista_LU[j]+"ATAACTTCGTATAATGTACATTATACGAAGTTAT"+"\n")
