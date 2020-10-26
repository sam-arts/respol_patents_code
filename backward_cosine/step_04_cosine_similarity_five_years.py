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

import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np


def my_tokenizer(s):
    return s.split()


def collect_blocks(d_blocks, ayear, n):
    inc = int(n/abs(n))
    ayears = list(range(ayear+inc, ayear+n+inc, inc))
    block = []
    for i in ayears:
        if i in d_blocks:
            block.extend(d_blocks[i])
    return block


def comp_sim(slice_start, slice_end, block_a, block_p, block_f):
    if block_p.shape[0] > 0:
        sim_p = block_a[slice_start:slice_end].dot(block_p.T).mean(axis=1)
        sim_p = np.squeeze(np.asarray(sim_p))
        if sim_p.shape:
            sim_p = list(sim_p)
        else:
            sim_p = [sim_p[()]]
    else:
        sim_p = [0]*block_a.shape[0]

    if block_f.shape[0] > 0:
        sim_f = block_a[slice_start:slice_end].dot(block_f.T).mean(axis=1)
        sim_f = np.squeeze(np.asarray(sim_f))
        if sim_f.shape:
            sim_f = list(sim_f)
        else:
            sim_f = [sim_f[()]]
    else:
        sim_f = [0]*block_a.shape[0]
    return sim_p, sim_f


data_dir = 'E:/data/2020_research_policy_replicate_results/'
idx_file = data_dir+'backward_cosine/keywords_all_idx.txt'
ayear_file = data_dir+'patent_ayear.txt'

# Reading patent data
print('Reading patent unigrams and patent numbers...')
d_ayear = {}
d_blocks = {}
d_pnos = {}
patents = []
pnos = []
i = 0
with open(idx_file, 'r', encoding='utf-8') as idx_reader,\
        open(ayear_file, 'r', encoding='utf-8') as ayear_reader:
    for line, line_ayear in zip(idx_reader, ayear_reader):
        tokens = line.strip().split(',')
        ayear = int(line_ayear.strip())
        if ayear not in d_ayear:
            d_ayear[ayear] = []
            d_blocks[ayear] = []
        pno = tokens[0]
        pnos.append(pno)
        patents.append(tokens[1])
        d_ayear[ayear].append(pno)
        d_blocks[ayear].append(i)
        i += 1
        if i % 1000000 == 0:
            print('\t '+str(i)+' patents read')
print('Patent unigrams and patent numbers read!')

print('Vectorizing patents to TF...')
vectorizer = CountVectorizer(analyzer=str.split)
patents_tf = vectorizer.fit_transform(patents)
print('Patents vectorized to TF!')

print('Normalizing TF matrix...')
patents_tf = normalize(patents_tf, norm='l2')
print('TF matrix normalized!')

del patents

l_ayear = list(d_ayear)
l_ayear.sort()
sequ = [0,    1,    2,    3,    4,    5,    6,    7,    8,    9,   10,   11,
        12,   13,   14,   15,   16]
inis = [1933, 1980, 1983, 1986, 1989, 1992, 1995, 1998, 2001, 2004, 2006, 2008,
        2010, 2012, 2014, 2016, 2018]
fins = [1980, 1983, 1986, 1989, 1992, 1995, 1998, 2001, 2004, 2006, 2008, 2010,
        2012, 2014, 2016, 2018, 2019]

print('Computing similarities...')
i = 8
cosine_file = data_dir+'backward_cosine/files/patent_cosine_all_'+str(i)+'.txt'
with open(cosine_file, 'w', encoding='utf-8') as cosine_writer:
    print('Block of years:', i)
    for ayear in range(inis[i], fins[i]):
        if ayear in d_ayear:
            start = time.time()
            print(ayear)
            idxs_current = d_blocks[ayear]
            block_current = patents_tf[idxs_current]
            block_past = collect_blocks(d_blocks, ayear, -5)
            block_past = patents_tf[block_past]
            block_future = collect_blocks(d_blocks, ayear, 5)
            block_future = patents_tf[block_future]

            results_past = []
            results_future = []
            rows_in_slice = 100
            slice_start = 0
            slice_end = slice_start + rows_in_slice
            while slice_end <= block_current.shape[0]:
                sim_p, sim_f = comp_sim(slice_start, slice_end, block_current,
                                        block_past, block_future)
                results_past.extend(sim_p)
                results_future.extend(sim_f)
                slice_start += rows_in_slice
                slice_end = slice_start + rows_in_slice

                if slice_start % 5000 == 0:
                    print('\t', slice_start)

            if slice_end > block_current.shape[0]:
                slice_end = block_current.shape[0]
                sim_p, sim_f = comp_sim(slice_start, slice_end, block_current,
                                        block_past, block_future)
                results_past.extend(sim_p)
                results_future.extend(sim_f)

            for pno, sim_past, sim_fut in zip(d_ayear[ayear], results_past,
                                              results_future):
                cosine_writer.write(pno + ',' + str(sim_past) + ',' +
                                    str(sim_fut) + '\n')
            end = time.time()
            print('Time for year ', ayear, ':', end-start)
end = time.time()
print('Total time:', end-start)
