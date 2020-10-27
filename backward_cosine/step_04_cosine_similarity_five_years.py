# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Computes the averegar cosine similarity of a focus patent
regarding the patents from 5 years in the past (backwward) and 5 years in
the future (forward). The output is a set of sequential files
patent_cosine_all_i.txt, where i is an index for the number of file. Each
file correspond to a set of years. In each file there are three columns, the
first one is the focus patent, the second the average backward cosine
similarity and the third one the average forward cosine similarity.

This code is part of the article: "Natural Language Processing to Identify the
Creation and Impact of New Technologies in Patent Text: Code, Data, and New
Measures"

"""

import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np


def my_tokenizer(s):
    """
    Split a string s by spaces.


    Parameters
    ----------
    s : The string.

    Returns
    -------
    s.split() : A list with the resulting substrings from the split

    """
    return s.split()


def collect_blocks(d_blocks, ayear, n):
    """
    Collect a block of patents for a window of n years regarding a focus
    year.
    If n is possitive the patents are from the future.
    If n is possitive the patents are from the past.


    Parameters
    ----------
    d_blocks : A dictionary of patent blocks, the key is the year, and the
              value is a list of indexes of the patents belongin to that year.
    ayear: The focus year
    n: The window size

    Returns
    -------
    block : A list with all the patents in the window of n years (past or
            or future)

    """
    inc = int(n/abs(n))
    ayears = list(range(ayear+inc, ayear+n+inc, inc))
    block = []
    for i in ayears:
        if i in d_blocks:
            block.extend(d_blocks[i])
    return block


def comp_sim(slice_start, slice_end, block_a, block_p, block_f):
    """
    Compute the similarity of a group of patents from block_a starting at
    slice_start and ending in slice_end regarding a block of patents from
    the past (block_p) and a block of patents from the future (bloc_f)


    Parameters
    ----------
    slice_start : The initial index to consider the group of patents
    slic_end : The final index to consider the group of patents
    block_a : An array containing the patent data to extract the group
    block_p : An array containing patents from the past
    block_f : An array containing patents from the future

    Returns
    -------
    sim_p : A sparse array with the similarities between the group of patents
            and the patents in the past
    sim_f : A sparse array with the similarities between the group of patents
            and the patents in the future

    """
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


data_dir = 'E:/data/2020_research_policy_replicate_results/' # Processed data
# Input common files
ayear_file = data_dir+'patent_ayear.txt'
# Output file for backward_cosine measure
idx_file = data_dir+'backward_cosine/keywords_all_idx.txt'

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

print('Computing similarities for 5 years window (past and future)...')
for i in sequ:
    cosine_file = data_dir+'backward_cosine/files/patent_cosine_all_'
    cosine_file += str(i)+'.txt'
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
                    sim_p, sim_f = comp_sim(slice_start, slice_end,
                                            block_current,
                                            block_past, block_future)
                    results_past.extend(sim_p)
                    results_future.extend(sim_f)
                    slice_start += rows_in_slice
                    slice_end = slice_start + rows_in_slice
    
                    if slice_start % 5000 == 0:
                        print('\t', slice_start)
    
                if slice_end > block_current.shape[0]:
                    slice_end = block_current.shape[0]
                    sim_p, sim_f = comp_sim(slice_start, slice_end,
                                            block_current,
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
print('Similarities computed!')
