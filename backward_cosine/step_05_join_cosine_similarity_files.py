# -*- coding: utf-8 -*-
"""
Created on Mon May 13 07:26:43 2019

@author: JC
"""

data_dir = 'E:/data/2020_research_policy_replicate_results/backward_cosine/'
sim_file = data_dir+'cosine_similarity.txt'
j = 0
with open(sim_file, 'w', encoding='utf-8') as sim_writer:
    for i in range(17):
        temp_file = data_dir+'files/patent_cosine_all_'+str(i)+'.txt'
        print(temp_file)
        with open(temp_file, 'r', encoding='utf-8') as temp_reader:
            for line in temp_reader:
                line = line.strip()
                sim_writer.write(line+'\n')
