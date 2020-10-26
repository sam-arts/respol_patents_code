# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Cleans the patent_concatenated.txt file by removing NLTK stop-
words, other common stopwords, greek letters, symbols and roman numerals.
Additionally it apply stemmming to each word using the SnowBall method
from NLTK. The output consists of two files, ngrams_[n]_vocabulary.txt, that
contains the list of all unique n-grams (beign n 2 or 3) in all the patents,
and ngrams_[n].txt, that contains the clean text for each patent. The text
is the list of unique n-grams for each patent.

This code is part of the article:

"""

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.util import ngrams
import operator
import re


def checkRoman(token):
    re_pattern = '[mdcxvi]+[a-z]'
    if re.fullmatch(re_pattern, token):
        return True
    return False


def checkword(w, stwrds):
    if ((len(w) > 1) and (w not in stwrds) and
            (not w.replace('-', '').isnumeric()) and (not checkRoman(w))):
        return True
    return False


aux_dir = 'E:/data/2019_patent_novelty_aux_files/'
data_dir = 'E:/data/2020_research_policy_replicate_results/'
# Common data for all processes
greek_file = aux_dir+'greek.txt'
symbol_file = aux_dir+'symbols.txt'
stop_file = aux_dir+'additional_stopwords.txt'
concat_file = data_dir+'patent_concatenated.txt'
pno_file = data_dir+'patent_number.txt'
# N-gram size (2 or 3)
n = 3
# N-gram output
voc_file = data_dir+'new_ngram/ngrams_'+str(n)+'_vocabulary.txt'
ngram_file = data_dir+'new_ngram/ngrams_'+str(n)+'.txt'

print('Reading patent numbers...')
patents = []
with open(pno_file, 'r') as pno_reader:
    for line in pno_reader:
        patents.append(line.strip())
print('Patent numbers read!')

print('Reading greek letters, symbols and stop words to remove...')
list_replace = []
with open(greek_file, 'r', encoding='utf-8') as greek_reader:
    greek_reader.readline()
    for line in greek_reader:
        tokens = line.strip().split(',')
        for token in tokens[1:-1]:
            if token != '-':
                tup = tuple((token, tokens[-1]))
                list_replace.append(tup)

with open(symbol_file, 'r', encoding='utf-8') as symbol_reader:
    for line in symbol_reader:
        tokens = line.strip().split(',')
        for token in tokens:
            tup = tuple((token, ' '))
            list_replace.append(tup)

stwrds = stopwords.words('english')
words = []
with open(stop_file, 'r', encoding='utf-8') as stop_reader:
    for line in stop_reader:
        words.append(line.strip())
stwrds.extend(words)
stwrds = set(stwrds)
print('Greek letters, symbols and stop words read!')

stemmer = SnowballStemmer("english")

d_ngrams = {}

print('Extracting '+str(n)+'-grams from patents...')
# This process could take several hours, depending on the computer
clean_patents = []
i = 0
with open(concat_file, 'r', encoding='utf-8') as concat_reader:
    for line in concat_reader:
        line = line.strip().lower()
        # Standardize greek letters and eliminate symbols
        for r in list_replace:
            line = line.replace(*r)
        # Replace .sub. and .sup.
        line = line.replace('.sub.', '')
        line = line.replace('.sup.', '')
        # Extract tokens using regular expression
        tokens = re.findall('[a-z0-9][a-z0-9-]*[a-z0-9]+|[a-z0-9]', line)

        # Extract ngrams
        n_grams = ngrams(tokens, n)

        # Check ngrams containg stopwords, roman numerals, words of only one
        # char, compossed only of numbers
        if n == 2:
            n_grams = [ngram for ngram in n_grams
                       if checkword(ngram[0], stwrds) and
                       checkword(ngram[1], stwrds)]
        else:
            n_grams = [ngram for ngram in n_grams
                       if checkword(ngram[0], stwrds) and
                       checkword(ngram[1], stwrds) and
                       checkword(ngram[2], stwrds)]
        # Unique ngrams
        n_grams = set(n_grams)

        # Stem tokens inside ngrams
        if n == 2:
            n_grams = [(stemmer.stem(w1), stemmer.stem(w2))
                       for w1, w2 in n_grams]
        else:
            n_grams = [(stemmer.stem(w1), stemmer.stem(w2), stemmer.stem(w3))
                       for w1, w2, w3 in n_grams]

        # Again unique ngrams
        n_grams = set(n_grams)

        # Store in the dictionary of patents
        clean_patents.append(n_grams)

        # Store in the dictionary of ngrams
        for ngram in n_grams:
            d_ngrams[ngram] = d_ngrams.get(ngram, 0) + 1

        i += 1
        if i % 100000 == 0:
            print('\t ', i, ' patents processed')
print(str(n)+'-grams extracted!')

# Clean ngrams appearing in only one patent
list_ngrams = list(d_ngrams)
d_dirty = {}
for ngram in list_ngrams:
    d_dirty[ngram] = d_ngrams[ngram]
    if d_ngrams[ngram] < 2:
        del d_ngrams[ngram]

voc_sorted = sorted(d_ngrams.items(), key=operator.itemgetter(1), reverse=True)

# Write the clean vocabulary
with open(voc_file, 'w', encoding='utf-8') as voc_writer:
    for ngram in voc_sorted:
        ngramstr = ' '.join(ngram[0])
        ngramstr += ' '+str(ngram[1])
        voc_writer.write(ngramstr+'\n')

# Clean patents using the vocabulary and write them
with open(ngram_file, 'w', encoding='utf-8') as ngram_writer:
    for n_grams, patent in zip(clean_patents, patents):
        if n == 2:
            text_wrt = ','.join([ngram[0]+' '+ngram[1]
                                 for ngram in n_grams if ngram in d_ngrams])
        else:
            text_wrt = ','.join([ngram[0]+' '+ngram[1]+' '+ngram[2]
                                 for ngram in n_grams if ngram in d_ngrams])
        ngram_writer.write(patent+','+text_wrt+'\n')
