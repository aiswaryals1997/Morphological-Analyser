# -*- coding: utf-8 -*-
"""generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HORhCc7F0lGMpkKNpDGqSAcSokf6BnXG
"""

from google.colab import files
uploaded = files.upload()

from google.colab import files
uploaded = files.upload()

import pandas as pd
import re
from collections import Counter
from math import sqrt
 
def word2vec(word):
    word_count = Counter(word)
    word_set = set(word_count)
    word_length = sqrt(sum(c*c for c in word_count.values()))
    print()
    return word_count, word_set, word_length
 
def cosine_distance(vector1, vector2):
    common = vector1[1].intersection(vector2[1])
    try:
        cosine_dist = sum(vector1[0][ch]*vector2[0][ch] for ch in common)/vector1[2]/vector2[2]
    except ZeroDivisionError:
        print("Oops!  That was not a valid input.  Try again...")
        return 0
       
    return cosine_dist
 
eng_sample =  pd.read_csv('Geng.csv', header=None, delimiter=',')
mal_sample = pd.read_csv('Gmal.csv', header=None, delimiter=',')
#print(malayalam_data)
eng_values = list(eng_sample[2])
df=pd.DataFrame(eng_values)
 
eng_roots = list(eng_sample[0])
mal_roots = list(mal_sample[0])
eng_suffix = list(eng_sample[1])
mal_suffix = list(mal_sample[1])
 
 
'''
[' കണ്ണൂർ', 'പൂച്ച', 'തല', 'മരുന്നു', 'താമര', 'രാജാവ്']
[' ൯െറ', 'യുടെ', 'യിൽ', 'കൾ', 'യുടെ', 'ൻ്റെ']
 
'''
# converting to lowercase values
 
pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
df_list=str(df)
vocab=pattern.findall(df_list.lower())
eng_roots_df = pd.DataFrame(eng_roots)
eng_roots_df_list=str(eng_roots_df)
lowercase_roots = pattern.findall(eng_roots_df_list.lower())
eng_suffix_df = pd.DataFrame(eng_suffix)
eng_suffix_df_list = str(eng_suffix_df)
lowercase_suffix = pattern.findall(eng_suffix_df_list.lower())
malayalam_values = list(mal_sample[2])
 
#establishing relation between english and malaayalam words using dictionary
 
dictionary = {vocab[i]: malayalam_values[i] for i in range(len(vocab))}  
root_dct = {mal_roots[i]: lowercase_roots[i] for i in range(len(vocab))}
suffix_dct = {mal_suffix[i]: lowercase_suffix[i] for i in range(len(vocab))}
 
#taking input from user
print('Enter root word:')
mal_root_inp = input()
root_input = [root_dct.get(mal_root_inp)] #selecting value from dictionary
#print(root_input)
 
print('Enter suffix word:')
mal_suffix_inp = input()
suffix_input = [suffix_dct.get(mal_suffix_inp)]
#print(suffix_input)
 
 
 
root_threshold = 0.80
 
suffix_threshold = 0.50
 
root_list = []    
 
#Fiding similar roots
for similar_roots in vocab:
    for word in root_input:
       
        try:
            result = cosine_distance(word2vec(word), word2vec(similar_roots))
            #print(word, '->', similar_roots,':', result*100)
 
            if result > root_threshold:
                 root_list.append(similar_roots)
                 print(word, '->', similar_roots,':', result*100)
        except IndexError:
            pass
       
       
           
#Fiding similar suffix
 
 
for similar_suffix in root_list:
    for word in suffix_input:
        try:
            suffix_result = cosine_distance(word2vec(word), word2vec(similar_suffix))
            print(word,'->', similar_suffix,':', suffix_result*100)
            if suffix_result > suffix_threshold:
                english_word=similar_suffix
        except IndexError:
            pass
       
 
                         
try:
    print('English word:',english_word)
    mal_word = dictionary.get(english_word)
 
    print('Malayalam word:', mal_word)
 
except NameError:  
    print("Oops!  That was not a valid input.  Try again...")