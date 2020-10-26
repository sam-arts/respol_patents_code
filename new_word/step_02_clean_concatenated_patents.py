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
from NLTK. It also removes words that appears in only one patent.
The output consists of two files, keywords_vocabulary.txt, that
contains the list of all unique unigrams in all the patents, and
keywords.txt, that contains the clean text for each patent. The text
is the list of unique unigrams for each patent.

This code is part of the article: "Natural Language Processing to Identify the
Creation and Impact of New Technologies in Patent Text: Code, Data, and New
Measures"

"""
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import operator
import re


def checkRoman(token):
    """
    Check if a token is a roman numeral.


    Parameters
    ----------
    token : A string.

    Returns
    -------
    True/False : A true value

    """    
    re_pattern = '[mdcxvi]+[a-z]'
    if re.fullmatch(re_pattern, token):
        return True
    return False


aux_dir = 'E:/data/2019_patent_novelty_aux_files/' # Original data
data_dir = 'E:/data/2020_research_policy_replicate_results/' # Processed data
greek_file = aux_dir+'greek.txt'
symbol_file = aux_dir+'symbols.txt'
stop_file = aux_dir+'additional_stopwords.txt'
# Input common files
concat_file = data_dir+'patent_concatenated.txt'
pno_file = data_dir+'patent_number.txt'
# Output files for new_word measure
voc_file = data_dir+'new_word/keywords_vocabulary.txt'
uni_file = data_dir+'new_word/keywords.txt'

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

stemmer = SnowballStemmer('english')

print('Cleaning patents...')
# This process could take several hours, depending on the computer
i = 0
clean_patents = []
with open(concat_file, 'r', encoding='utf-8') as concat_reader:
    for line in concat_reader:
        line = line.strip().lower()
        # Standardize greek letters and eliminate symbols
        for r in list_replace:
            line = line.replace(*r)
        # Replace .sub. and .sup. in each patent
        line = line.replace('.sub.', '')
        line = line.replace('.sup.', '')
        # Extract tokens using a regular expression
        tokens = re.findall('[a-z0-9][a-z0-9-]*[a-z0-9]+|[a-z0-9]', line)
        tokens = set(tokens)
        # Remove stopwords, and words of only one char and compossed only
        # of numbers
        tokens = [token for token in tokens if len(token) > 1 and
                  token not in stwrds and
                  not token.replace('-', '').isnumeric()]
        tokens = [stemmer.stem(token) for token in tokens]
        tokens = set(tokens)
        tokens = list(tokens)
        tokens.sort()
        tokens = [token for token in tokens if len(token) > 1 and
                  token not in stwrds and
                  not checkRoman(token)]
        clean_patents.append(tokens)
        i += 1
        if i % 100000 == 0:
            print('\t '+str(i)+' patents processed')
print('Patents cleaned!')

print('Forming and cleaning vocabulary...')
d_words = {}
for tokens in clean_patents:
    for token in tokens:
        d_words[token] = d_words.get(token, 0) + 1

# Eliminate words appearing in only one patent
list_words = list(d_words)
d_dirty = {}
for word in list_words:
    d_dirty[word] = d_words[word]
    if d_words[word] < 2:
        del d_words[word]
print('Vocabulary formed!')

print('Cleaning patent data using the vocabulary...')
# Eliminate words not in clean vocabulary
for i in range(len(clean_patents)):
    tokens = clean_patents[i]
    tokens_clean = [token for token in tokens if token in d_words]
    clean_patents[i] = tokens_clean
print('Patent data cleaned!')

voc_sorted = sorted(d_words.items(), key=operator.itemgetter(1), reverse=True)

print('Saving vocabulary...')
# Write vocabulary
with open(voc_file, 'w', encoding='utf-8') as voc_writer:
    for pair in voc_sorted:
        voc_writer.write(pair[0]+' '+str(pair[1])+'\n')
print('Vocabulary saved!')

print('Saving patent data...')
# Save patent number and patent text
with open(uni_file, 'w', encoding='utf-8') as uni_writer:
    for tokens, patent in zip(clean_patents, patents):
        line = ' '.join(tokens)
        uni_writer.write(patent+','+line+'\n')
print('Patent data saved!')
