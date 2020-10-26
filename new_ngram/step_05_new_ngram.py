# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Finds the new ngrams from a focus patent, considering all the
ngrams from patents in the past and the baseline dictionary. The ngrams are
extracted and considered only for patents filed from 1980 onwards. The output
is new_ngram_[n].txt, containing the list of new ngrams found in patents,
the first patent to use it (patent number) and the total number of patents
using it.

This code is part of the article:

"""


def read_file(file):
    """
    Reads a file line by line and stores them in a list.


    Parameters
    ----------
    file : The file to read. Each line in the file represents an element to be
    stored in a list.

    Returns
    -------
    content : A list with the lines of the file as elements.

    """
    content = []
    with open(file, 'r', encoding='utf-8') as reader:
        for line in reader:
            line = line.strip()  # Remove the newline char
            content.append(line)
    return content


data_dir = 'E:/data/2020_research_policy_replicate_results/'
# N-gram size (2 or 3)
n = 2
# Input general file
ayear_file = data_dir+'patent_ayear.txt'
# Input ngrams file
idx_file = data_dir+'new_ngram/ngrams_'+str(n)+'_idx.txt'
voc_file = data_dir+'new_ngram/ngrams_'+str(n)+'_vocabulary.txt'
base_voc_file = data_dir+'new_ngram/ngrams_'+str(n)+'_baseline_vocabulary.txt'
# Output ngrams file
new_ngram_file = data_dir+'new_ngram/new_ngram_'+str(n)+'.txt'

print('Loading baseline '+str(n)+'-ngram vocabulary')
baseline_voc = read_file(base_voc_file)
print('Baseline '+str(n)+'-ngram vocabulary loaded')

baseline_voc = set(baseline_voc)  # Cast to set for faster access

new_ngram = {}

print('Finding new '+str(n)+'-gram per patent...')
i = 0
with open(ayear_file, 'r', encoding='utf-8') as ayear_reader,\
        open(idx_file, 'r', encoding='utf-8') as idx_reader:
    for line_ayear, line_idx in zip(ayear_reader, idx_reader):
        ayear = int(line_ayear.strip())
        if ayear >= 1980:
            tokens = line_idx.strip().split(',')
            pno = tokens[0]
            tokens = tokens[1].split()
            for ngram in tokens:
                if (ngram not in baseline_voc) and (ngram not in new_ngram):
                    new_ngram[ngram] = [pno, 0]
                if ngram in new_ngram:
                    new_ngram[ngram][1] += 1
        i += 1
        if i % 100000 == 0:
            print('\t '+str(i)+' patents processed')
print('New '+str(n)+'-gram found!')

print('Reading whole vocabulary...')
whole_voc = read_file(voc_file)
print('whole vocabulary read!')

# Inverted index for vocabulary idx:word
i = 0
voc = {}
for line in whole_voc:
    tokens = line.strip().split()
    ngram = ' '.join([token for token in tokens[:n]])
    voc[i] = ngram
    i += 1

print('Saving new ngrams...')
with open(new_ngram_file, 'w', encoding='utf-8') as new_ngram_writer:
    new_ngram_writer.write('ngram,patent,freq\n')
    for ngram in new_ngram:
        pno = new_ngram[ngram][0]
        count = new_ngram[ngram][1]
        ngram = int(ngram)
        new_ngram_writer.write(voc[ngram]+','+pno+','+str(count)+'\n')
print('New words saved!')
