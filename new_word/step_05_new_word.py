# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Finds the new words from a focus patent, considering all the
words from patents in the past and the baseline dictionary. The words are
extracted and considered only for patents filed from 1980 onwards. The output
is new_keywords.txt, containing the list of new words found in a patent,
the first patent to use it (patent number) and the total number of patents
using it.

This code is part of the article: "Natural Language Processing to Identify the
Creation and Impact of New Technologies in Patent Text: Code, Data, and New
Measures"

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


data_dir = 'E:/data/2020_research_policy_replicate_results/' # Processed data
# Input common files
ayear_file = data_dir+'patent_ayear.txt'
# Input files from new_word measure
idx_file = data_dir+'new_word/keywords_idx.txt'
voc_file = data_dir+'new_word/keywords_vocabulary.txt'
base_voc_file = data_dir+'new_word/keywords_baseline_vocabulary.txt'
# Output file for new_word measure
new_word_file = data_dir+'new_word/new_keywords.txt'

print('Reading baseline vocabulary...')
baseline_voc = read_file(base_voc_file)
print('Baseline vocabulary read!')

baseline_voc = set(baseline_voc)  # Cast to set for faster access


new_word = {}

print('Finding new words per patent...')
i = 0
with open(ayear_file, 'r', encoding='utf-8') as ayear_reader,\
        open(idx_file, 'r', encoding='utf-8') as idx_reader:
    for line_ayear, line_idx in zip(ayear_reader, idx_reader):
        ayear = int(line_ayear.strip())
        if ayear >= 1980:
            tokens = line_idx.strip().split(',')
            pno = tokens[0]
            tokens = tokens[1].split()
            for word in tokens:
                if (word not in baseline_voc) and (word not in new_word):
                    new_word[word] = [pno, 0]
                if word in new_word:
                    new_word[word][1] += 1
        i += 1
        if i % 100000 == 0:
            print('\t '+str(i)+' patents processed')
print('New words found!')

print('Reading whole vocabulary...')
whole_voc = read_file(voc_file)
print('whole vocabulary read!')

# Inverted index for vocabulary idx:word
i = 0
voc = {}
for word in whole_voc:
    voc[i] = word.split()[0]
    i += 1

print('Saving new words...')
with open(new_word_file, 'w', encoding='utf-8') as new_word_writer:
    new_word_writer.write('word,patent,freq\n')
    for word in new_word:
        pno = new_word[word][0]
        count = new_word[word][1]
        word = int(word)
        new_word_writer.write(voc[word]+','+pno+','+str(count)+'\n')
print('New words saved!')
