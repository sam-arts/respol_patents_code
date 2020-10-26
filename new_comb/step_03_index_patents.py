# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Indexs the patent unigrams using the vocabulary. This is done to
speed up the comparison process to find the first patent using an unigram and
all the patents using such unigram. The outputs is keywords_idx.txt,
that contains the index of each unigram as in the vocabulary.

This is the same code as in new_word/step_03_index_patents.py and
produces the same output in the same directory new_word/.

This code is part of the article:

"""

data_dir = 'E:/data/2020_research_policy_replicate_results/'
# new_word input
uni_file = data_dir+'new_word/keywords.txt'
voc_file = data_dir+'new_word/keywords_vocabulary.txt'
# new_word output
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
