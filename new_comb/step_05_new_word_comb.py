# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Finds the new combinations of n words from a focus patent, consi-
dering all the word combinations from patents in the past and the baseline di-
ctionary. The words are extracted and considered only for patents filed from
1980 onwards. The output is new_keyword_combinations_[n].txt, containing the
list of new combinations of n words found in a patent, the first patent to use
them (patent number) and the total number of patents using them.

This code is part of the article: "Natural Language Processing to Identify the
Creation and Impact of New Technologies in Patent Text: Code, Data, and New
Measures"

"""
import itertools as it


data_dir = 'E:/data/2020_research_policy_replicate_results/' # Processed data
# Size of word combination (2 or 3)
n = 2
# Input common file
ayear_file = data_dir+'patent_ayear.txt'
# Input files from new_word measure
idx_file = data_dir+'new_word/keywords_idx.txt'
voc_file = data_dir+'new_word/keywords_vocabulary.txt'
# Input file from new_comb measure
base_voc_file = data_dir+'new_comb/comb_'+str(n)+'_baseline_vocabulary.txt'
# Output file for new_comb measure
new_comb_file = data_dir+'new_comb/new_keyword_combinations_'+str(n)+'.txt'

print('Reading baseline vocabulary...')
baseline_voc = []
with open(base_voc_file, 'r', encoding='utf-8') as base_voc_reader:
    for line in base_voc_reader:
        line = line.strip().split(',')  # Remove newline char and split line
        comb = [int(token) for token in line]
        comb = tuple(comb)
        baseline_voc.append(comb)
print('Baseline vocabulary read!')

baseline_voc = set(baseline_voc)  # Cast to set for faster access

new_word_comb = {}

# This process could take some time, depending on the computer
print('Finding new word combinations per patent...')
i = 0
with open(ayear_file, 'r', encoding='utf-8') as ayear_reader,\
        open(idx_file, 'r', encoding='utf-8') as idx_reader:
    for line_ayear, line_idx in zip(ayear_reader, idx_reader):
        ayear = int(line_ayear.strip())
        if ayear >= 1980:
            line_idx = line_idx.strip()  # Remove newline char
            tokens = line_idx.split(',')  # Split line
            pno = tokens[0]
            # Cast word idxs to int
            tokens = [int(idx) for idx in tokens[1].split()]
            word_comb = it.combinations(tokens, n)  # Extract combinations
            for word_comb in word_comb:
                if (word_comb not in baseline_voc) and (word_comb not in
                                                        new_word_comb):
                    new_word_comb[word_comb] = [pno, 0]
                if word_comb in new_word_comb:
                    new_word_comb[word_comb][1] += 1
        i += 1
        if i % 100000 == 0:
            print('\t '+str(i)+' patents processed')
print('New word combinations found!')

# Inverted index for vocabulary idx:word
print('Reading whole vocabulary...')
voc = {}
i = 0
with open(voc_file, 'r', encoding='utf-8') as voc_reader:
    for line in voc_reader:
        word = line.strip().split()[0]  # Remove newline char and split line
        voc[i] = word
        i += 1
print('whole vocabulary read!')

print('Saving new word combinations...')
with open(new_comb_file, 'w', encoding='utf-8') as new_comb_writer:
    header = 'word_'+'word_'.join([str(i)+',' for i in range(1, n+1)])
    new_comb_writer.write(header+'patent,freq\n')
    for word_comb in new_word_comb:
        pno = new_word_comb[word_comb][0]
        count = new_word_comb[word_comb][1]
        comb = ','.join([voc[word] for word in word_comb])
        new_comb_writer.write(comb+','+pno+','+str(count)+'\n')
print('New word combinations saved!')
