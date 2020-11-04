# This code is part of the article: "Natural Language Processing to Identify the Creation and Impact of New Technologies in Patent Text: Code, Data, and New Measures"

To use the code to replicate the results in the paper, the following steps need to be followed:

1. Create an auxiliary data directory with the original raw data files as input: claim_full_till2018.csv and patent_title_abstract_till_2018.csv
2. Create a data directory to store the outputs from the code
3. Run the step_01_concatenate_patents.py code to concatenate the raw files
4. There are 5 metrics to compute with the code: new_word, new_word_comb, new_bigram, new_trigram and backward_cosine. For each, there is a folder with the required steps to compute it. The metrics new_bigram and new_trigram use the code in the new_ngram folder.
5. Inside each code folder the requiered steps to compute a metric are numbered sequentially, and they must be run in that order.
6. Inside the data directory create a folder for each metric to store the corresponding output files.
