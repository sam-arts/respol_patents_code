# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Extract a baseline vocabulary of ngrams. The vocabulary is
formed by all the unique ngrams from patents filed before 1980. The outputs is
ngrams_[n]_baseline_vocabulary.txt, that contains the list of ngrams from
patents before 1980, with n as the size of the ngrams (2 or 3)


This code is part of the article:

"""

data_dir = 'E:/data/2020_research_policy_replicate_results/'
# N-gram size (2 or 3)
n = 3
# Input common file
ayear_file = data_dir+'patent_ayear.txt'
# Input ngrams file
idx_file = data_dir+'new_ngram/ngrams_'+str(n)+'_idx.txt'
# Output ngrams file
base_voc_file = data_dir+'new_ngram/ngrams_'+str(n)+'_baseline_vocabulary.txt'

print('Building baseline vocabulary...')
voc = {}
i = 0
with open(idx_file, 'r', encoding='utf-8') as idx_reader,\
        open(ayear_file, 'r', encoding='utf-8') as ayear_reader:
    for line_idx, line_ayear in zip(idx_reader, ayear_reader):
        ayear = int(line_ayear.strip())
        if ayear < 1980:
            tokens = line_idx.strip().split(',')  # Remove the newline char
            tokens = tokens[1].split()  # Split tokens
            for token in tokens:
                voc[token] = 0
        i += 1
        if i % 100000 == 0:
            print('\t '+str(i)+' patents processed')
print('Baseline vocabulary built!')

print('Saving baseline vocabulary...')
with open(base_voc_file, 'w', encoding='utf-8') as base_voc_writer:
    for word in voc:
        base_voc_writer.write(word+'\n')
print('Baseline vocabulary saved!')
