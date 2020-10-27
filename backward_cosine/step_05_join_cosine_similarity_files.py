# -*- coding: utf-8 -*-
"""
Created on Mon Aug 3 14:15:00 2020

@authors: Juan Carlos Gomez
          Sam Arts
          Jianan Hou

@emails: jc.gomez@ugto.mx
         sam.arts@kuleuven.be
         jianan.hou@kuleuven.be

@description: Merges the sequence of cosine similarity files
patent_cosine_all_i.txt, where i is an index for the number of file. Each
file correspond to a set of years. The output is cosine_similarity.txt as the
sequential merge of all the files.

This code is part of the article: "Natural Language Processing to Identify the
Creation and Impact of New Technologies in Patent Text: Code, Data, and New
Measures"

"""

data_dir = 'E:/data/2020_research_policy_replicate_results/' # Processed data
# Output file for backward_cosine measure
sim_file = data_dir+'backward_cosine/cosine_similarity.txt'
j = 0
print('Merging the cosine similarity files...')
with open(sim_file, 'w', encoding='utf-8') as sim_writer:
    for i in range(17):
        temp_file = data_dir+'files/patent_cosine_all_'+str(i)+'.txt'
        print(temp_file)
        with open(temp_file, 'r', encoding='utf-8') as temp_reader:
            for line in temp_reader:
                line = line.strip()
                sim_writer.write(line+'\n')
print('Cosine similarity files merged!')
