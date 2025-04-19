#Requires seqkit
import argparse
import os
import re
import regex as re

#USAGE:python find_amplicons.py -f primers_fwd.txt -r primers_rev_com.txt -file SynIII_reference_sline.fa -a assembly.fasta


parser= argparse.ArgumentParser(description="Read input files")
parser.add_argument("--fwd","-f",
        metavar="FILE",
        required=True,
        help="fasta file the genome or sample to divide into LU's ")
parser.add_argument("--rev","-r",
        required=True)
parser.add_argument("--file","-file",
        required=True)
parser.add_argument("--assembly","-a",
        required=True)


args=parser.parse_args()
name_input=args.file.split('.fa')
name_input=name_input[0]
name_salida=name_input+"_seqkit"
list_fwd=[]
list_rev=[]
with open(args.fwd,'r') as f_fwd:
    for line_f in f_fwd.readlines():
        line_f=line_f.strip()
        list_fwd.append(line_f)

#print(list_fwd)
with open(args.rev, 'r') as f_rev:
    for line_r in f_rev.readlines():
        line_r=line_r.strip()
        list_rev.append(line_r)
#print(list_rev)

lista=[]
with open(name_input+'.fa','r') as sample, open("out_coordinates.txt",'w') as out_s:
    for linea in sample.readlines():
        for i in range(0,len(list_fwd)):
            for k in range(0,len(list_rev)):
                if i == k:
                    pattern_i=re.compile(str(list_fwd[i]),re.I)
                    pattern_k=re.compile(str(list_rev[k]),re.I)
                    if pattern_i.finditer(linea) and pattern_k.finditer(linea):
                        result = pattern_i.finditer(linea)
                        result_2 = pattern_k.finditer(linea)
                        for match_obj in result:
                            for match_obj_2 in result_2:
                                #print(match_obj,match_obj_2)
                                start= match_obj.span()[0]
                                end= match_obj_2.span()[1]
                                #print (start,end)
                                print()
                                out_s.write( "seqkit subseq -r %s:%s %s\n" %(start,end,args.file))
                else:
                    pass
os.system("cat out_coordinates.txt | parallel | tee %s_extracted_amplicons.fa " %name_input)
os.system("awk '/>/{sub(/syn/,++i)}1' %s_extracted_amplicons.fa > %s_extracted_amplicons_num.fa"%(name_input,name_input))
database="%s_extracted_amplicons_num.fa"  %name_input
def my_blastn(assembly,database):
    out_db=database.split(".fa")
    out_db=out_db[0]
    out_db=str(out_db)+"DB"
    out_blastn=assembly.split(".fasta")
    out_blastn=out_blastn[0]
    out_blastn=str(out_blastn)+".blastn"
    print("makeblastdb -in %s -parse_seqids -dbtype nucl -out %s" % (database, out_db))
    os.system("makeblastdb -in %s -parse_seqids -dbtype nucl -out %s" % (database,out_db))
    print("======================BlastN==========================")
    os.system("blastn -query %s -db %s -out %s -outfmt 6 -evalue 1e-50" % (assembly,out_db,out_blastn))
    print("blastn -query %s -db %s -out %s -evalue 1e-50 -outfmt '6 qseqid sseqid pident length gapopen qstart qend sstart send evalue bitscore gaps' " % (assembly,out_db,out_blastn))

my_blastn( assembly= args.assembly, database= database)


'''To run afterwards:
#for i in ls *.blastn; do sort -k 2 -n "$i" > "$i"_sorted.txt; done 
'''
