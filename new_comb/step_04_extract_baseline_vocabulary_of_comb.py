# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Extract a baseline vocabulary of indexed word combinations using
the file keywords_idx.txt. The vocabulary is formed by all the unique indexed
word combinations from patents filed before 1980. The output is
comb_[n]_baseline_vocabulary.txt, that contains the list of combinations of
n words from patents before 1980. n is the number of words in the combination
(2 or 3).

This code needs the data produced in the previous steps and stored in the
new_word/ directory.

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
# Input file from new_word measure
idx_file = data_dir+'new_word/keywords_idx.txt'
# Output file for new_comb measure
base_voc_file = data_dir+'new_comb/comb_'+str(n)+'_baseline_vocabulary.txt'

# This process could take some time, depending on the computer
print('Building baseline vocabulary of word combinations...')
voc = {}
i = 0
with open(idx_file, 'r', encoding='utf-8') as idx_reader,\
        open(ayear_file, 'r', encoding='utf-8') as ayear_reader:
    for line_idx, line_ayear in zip(idx_reader, ayear_reader):
        ayear = int(line_ayear.strip())
        if ayear < 1980:
            line_idx = line_idx.strip()  # Remove newline char
            tokens = line_idx.split(',')  # Split tokens
            # Cast word idxs to int
            tokens = [int(idx) for idx in tokens[1].split()]
            word_combs = it.combinations(tokens, n)  # Extract combinations
            for j, word_comb in enumerate(word_combs):
                voc[word_comb] = 0
        i += 1
        if i % 100000 == 0:
            print('\t '+str(i)+' patents processed')
print('Baseline vocabulary built!')

print('Saving baseline vocabulary of word combinations...')
with open(base_voc_file, 'w', encoding='utf-8') as base_voc_writer:
    for word_comb in voc:
        comb = ','.join([str(word) for word in word_comb])
        base_voc_writer.write(comb+'\n')
print('Baseline vocabulary saved!')
