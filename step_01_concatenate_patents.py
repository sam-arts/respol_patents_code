# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Concatenates title, abstract and claims from a patent in a
collection of patents. The data comes from two files, claim_fill_till2018.csv,
that contains the claims per patent, and patent_title_abstract_till_2018.csv,
that contains the title and abstract per patent. The claims for a patent
encompass several rows, the title and abstract are in the same row. The inde-
xing of claims is removed (e.g. a. a.1. 1.a. etc). The output consists of four
files, patent_concatenated.txt, with the patent data concatenated, and
patent_number.txt with the patent number, patent_adate.txt, with
the patent filling date, patent_ayear.txt with the patent filling year, the
last three files are in correspondance 1 to 1 with patent_concatenated.txt.

This code load all the data in memory, so be sure to have enough memory in
your computer (> 32 GB)

This code is part of the article: "Natural Language Processing to Identify the
Creation and Impact of New Technologies in Patent Text: Code, Data, and New
Measures"

"""

import pandas as pd
import math as mt
import re


data_dir = 'E:/data/2019_patent_novelty_aux_files/'  # Data directory
out_dir = 'E:/data/2020_research_policy_replicate_results/'  # Output directory
claims_file = data_dir+'claim_full_till2018.csv'
title_abstract_file = data_dir+'patent_title_abstract_till_2018.csv'
pno_file = out_dir+'patent_number.txt'
concat_file = out_dir+'patent_concatenated.txt'
adate_file = out_dir+'patent_adate.txt'
ayear_file = out_dir+'patent_ayear.txt'

print('Reading claims from CSV...')
claims_data = pd.read_csv(claims_file)
claims_data['claim_txt'] = claims_data['claim_txt'].astype(str)
print('Claims read!')

d_text = {}

print('Concatenating claims from CSV...')
i = 0
for row in claims_data.itertuples():
    line = ''
    if row.claim_txt != 'nan':
        tokens = row.claim_txt.split()
        first = tokens[0]
        if re.match('\'?.?[0-9]+.?', first) or re.match(';?[a-z].', first):
            tokens = tokens[1:]
        line = ' '.join([token for token in tokens])
    if row.patent not in d_text:
        d_text[row.patent] = ''
    d_text[row.patent] += line+' '
    i += 1
    if i % 1000000 == 0:
        print('\t '+str(i)+' patents processed')
print('Claims concatenated!')

print('Reading title and abstract from CSV...')
title_data = pd.read_csv(title_abstract_file)
title_data['filing_date'] = title_data['filing_date'].astype(str)
title_data['grant_date'] = title_data['grant_date'].astype(str)
title_data['abstract'] = title_data['abstract'].astype(str)
title_data['title'] = title_data['title'].astype(str)
print('Title and abstract read!')


print('Concatenating title and abstract...')
i = 0
adates = {}
ayears = {}
l_tuples = []
for row in title_data.itertuples():
    line = ''
    if row.title != 'nan':
        line += ' '+row.title
    if row.abstract != 'nan':
        line += ' '+row.abstract
    if row.patent in d_text:
        line += ' '+d_text[row.patent]
    d_text[row.patent] = line
    adates[row.patent] = row.adate
    ayears[row.patent] = row.ayear
    # Form a tuple with adate, patent number and ayear to sort the patents
    # first by adate and then by patent number
    l_tuples.append((row.adate, row.patent, row.ayear))
    i += 1
    if i % 1000000 == 0:
        print('\t '+str(i)+' patents processed')
print('Title and abstract concatenated!')

l_tuples.sort()

print('Saving patent data sorted by adate and patent number...')
with open(pno_file, 'w', encoding='utf-8') as pno_writer,\
        open(concat_file, 'w', encoding='utf-8') as concat_writer,\
        open(ayear_file, 'w', encoding='utf-8') as ayear_writer,\
        open(adate_file, 'w', encoding='utf-8') as adate_writer:
    for tup in l_tuples:
        patent = tup[1]
        pno_writer.write(str(patent)+'\n')
        concat_writer.write(d_text[patent]+'\n')
        ayear_writer.write(str(ayears[patent])+'\n')
        if mt.isnan(adates[patent]):
            adate_writer.write('nan\n')
        else:
            adate_writer.write(str(int(adates[patent]))+'\n')
print('Patent data saved!')
