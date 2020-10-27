# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Indexs the patent unigrams in the file keywords.txt using the
vocabulary in keywords_vocabulary.txt. This is done to
speed up the comparison process in the following steps. The output is 
keywords_idx.txt, that contains the index of each unigram as in the vocabulary.

This code is part of the article: "Natural Language Processing to Identify the
Creation and Impact of New Technologies in Patent Text: Code, Data, and New
Measures"

"""

data_dir = 'E:/data/2020_research_policy_replicate_results/' # Processed data
# Input files from new_word measure
uni_file = data_dir+'new_word/keywords.txt'
voc_file = data_dir+'new_word/keywords_vocabulary.txt'
# Output file for new_word measure
idx_file = data_dir+'new_word/keywords_idx.txt'

print('Reading vocabulary...')
voc = {}
i = 0
with open(voc_file, 'r', encoding='utf-8') as voc_reader:
    for line in voc_reader:
        tokens = line.strip().split()
        # Each word in the vocabulary is indexed sequentially
        voc[tokens[0]] = i
        i += 1
print('Vocabulary read!')

print('Indexing and saving patents...')
i = 0
with open(uni_file, 'r', encoding='utf-8') as uni_reader,\
        open(idx_file, 'w', encoding='utf-8') as idx_writer:
    for line in uni_reader:
        tokens = line.strip().split(',')
        pno = tokens[0]
        tokens = tokens[1].split()
        # Index the words
        tokens = [voc[token] for token in tokens]
        tokens.sort()
        patent_indexed = ' '.join([str(token) for token in tokens])
        idx_writer.write(pno+','+patent_indexed+'\n')
        i += 1
        if i % 100000 == 0:
            print('\t '+str(i)+' patents indexed')
print('Patents indexed and saved!')
