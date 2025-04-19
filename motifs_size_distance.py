#!usr/bin/env python3
# -- coding: utf-8 --
#
# ------------------------------
# Name: Compare_rev_fwd 
# Purpose:
# Compare the location where the motifs were found and calculate the distance or size of the amplicon
# Author: Maria del Carmen Sanchez
# USAGE: python compare_rev_fwd.py output_fwd.txt output_rev.txt
# Created: April,2023
# ------------------------------
import sys
from collections import defaultdict
fwd_file=sys.argv[1]
rev_file=sys.argv[2]
d_rev=defaultdict(list)
d_fwd=defaultdict(list)
values_fwd=[]
import pandas as pd
values_fwd=open(fwd_file).readlines()
for i in values_fwd:
    if i.startswith('Primer'):
        pass
    else:
        i=i.split('\t')
        d_fwd[i[0]] ##Declaring the key of the dictionary
        # Declaring the values for every key
        d_fwd[i[0]].append(i[1]) # Value:start
        d_fwd[i[0]].append(i[2]) # Value:end
        d_fwd[i[0]].append(i[3]) # Value:strand
        d_fwd[i[0]].append(i[4])# Value: score
        d_fwd[i[0]].append(i[-1]) # Value:scaffold or contig
#print(d_fwd.items())
values_rev=open(rev_file).readlines()
for i in values_rev:
    if i.startswith('Primer'):
        pass
    else:
        i=i.split('\t')
        d_rev[i[0]] ##Declaring the key of the dictionary
        # Declaring the values for every key
        d_rev[i[0]].append(i[1]) # Value:start
        d_rev[i[0]].append(i[2]) # Value:end
        d_rev[i[0]].append(i[3]) # Value:strand
        d_rev[i[0]].append(i[4])# Value: score
        d_rev[i[0]].append(i[-1]) # Value:scaffold or contig
#print(d_rev.items())
list_oligos=[]
list_values=[]
for key_fwd,value1 in d_fwd.items():
    for key_rev,value2 in d_rev.items():
        if key_fwd==key_rev:
            list_oligos.append(key_fwd)
            if value1[4] == value2[4]:
            #print(value1[4], value2[4])
            amplicon_size=abs(int(value1[0])-int(value2[1]))
            print(key_rev,amplicon_size)
            if amplicon_size > 700:
               print(key_rev,'0')
               #print(amplicon_size)
               list_values.append('0')
            else:
                print(key_rev,'1')
                list_values.append('1')
            if value1[3] == '+' and value2[3] == '-':
                orientation = '+'
            elif value1[3] == '-' and value2[3] == '+':
                orientation = '-'

with open("in_silico_pcr_output.txt", 'a') as outfile:
    outfile.write("Name" + "\t" + ', '.join(map(str, list_oligos)) + "\n")
    outfile.write("Name"  + "\t" + ', '.join(map(str, list_values)) + "\n")
